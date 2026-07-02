from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

# ============================================
# STEP 1: CONFIGURATION - UPDATE THIS!
# ============================================
# TODO: Replace with YOUR admission number
ADMISSION_NUMBER = "C027-01-0860/2024"

# ============================================
# STEP 2: DETERMINE YOUR DATASET (AUTO-CALCULATED)
# ============================================
# Extract the last digit
last_digit = int(ADMISSION_NUMBER.split("/")[0].split("-")[-1][-1])

# Extract the xxxx number
xxxx = int(ADMISSION_NUMBER.split("/")[0].split("-")[-1])

# Check if xxxx is even
is_even = xxxx % 2 == 0

# Extract first two digits
first_two_digits = int(str(xxxx)[:2])

# Calculate number of gigs
NUM_GIGS = 5 + last_digit

# Determine categories
if is_even:
    CATEGORIES = ["Development", "Design", "Writing"]
else:
    CATEGORIES = ["Marketing", "Data", "Consulting"]

# Determine currency
CURRENCY = "KES" if first_two_digits < 10 else "USD"

# ============================================
# STEP 3: FASTAPI APP INITIALIZATION
# ============================================
app = FastAPI(
    title="GigHub API",
    description=f"Nairobi Freelance Gigs Platform - {ADMISSION_NUMBER}",
    version="1.0.0"
)

# ============================================
# STEP 4: CREATE YOUR GIGS DATABASE
# ============================================
# Note: You must create exactly NUM_GIGS gigs
# If NUM_GIGS = 9, create 9 gigs

gigs_db = [
    {
        "id": 1,
        "title": "Build a React Dashboard",
        "description": "Build a React dashboard for a fintech startup. Must be responsive and mobile-friendly.",
        "category": "Development",
        "budget": 15000.0,
        "currency": CURRENCY,
        "status": "Open",
        "client_name": "Jane Muthoni"
    },
    {
        "id": 2,
        "title": "Design a Mobile App UI",
        "description": "Create UI/UX designs for a mobile app using Figma. Must include wireframes and prototypes.",
        "category": "Design",
        "budget": 12000.0,
        "currency": CURRENCY,
        "status": "Open",
        "client_name": "John Kamau"
    },
    {
        "id": 3,
        "title": "Write Technical Documentation",
        "description": "Write comprehensive documentation for a Python API. Must include setup guides and API reference.",
        "category": "Writing",
        "budget": 8000.0,
        "currency": CURRENCY,
        "status": "Open",
        "client_name": "Mary Wanjiru"
    },
    {
        "id": 4,
        "title": "Full Stack E-commerce Website",
        "description": "Develop a full stack e-commerce website using Django and React. Must include payment integration.",
        "category": "Development",
        "budget": 35000.0,
        "currency": CURRENCY,
        "status": "Open",
        "client_name": "Peter Ochieng"
    },
    {
        "id": 5,
        "title": "Logo Design for Startup",
        "description": "Design a modern logo for a tech startup. Must include multiple variations and color schemes.",
        "category": "Design",
        "budget": 5000.0,
        "currency": CURRENCY,
        "status": "In Progress",
        "client_name": "Sarah Akinyi"
    },
    {
        "id": 6,
        "title": "Content Writing for Blog",
        "description": "Write 10 blog posts about technology trends. Each post must be at least 1000 words.",
        "category": "Writing",
        "budget": 15000.0,
        "currency": CURRENCY,
        "status": "Open",
        "client_name": "David Mwangi"
    },
    {
        "id": 7,
        "title": "Mobile App Development",
        "description": "Build a cross-platform mobile app using Flutter. Must work on both iOS and Android.",
        "category": "Development",
        "budget": 45000.0,
        "currency": CURRENCY,
        "status": "Open",
        "client_name": "Grace Njeri"
    },
    {
        "id": 8,
        "title": "Social Media Graphics",
        "description": "Create social media graphics for a marketing campaign. Must include 20+ designs.",
        "category": "Design",
        "budget": 7500.0,
        "currency": CURRENCY,
        "status": "Closed",
        "client_name": "James Omondi"
    },
    {
        "id": 9,
        "title": "Technical Ebook Writing",
        "description": "Write an ebook about Python programming for beginners. Must include examples and exercises.",
        "category": "Writing",
        "budget": 25000.0,
        "currency": CURRENCY,
        "status": "Open",
        "client_name": "Ann Wambui"
    }
]

# ============================================
# STEP 5: PYDANTIC MODELS
# ============================================

class GigCreate(BaseModel):
    """Model for creating a new gig"""
    title: str = Field(..., min_length=5, max_length=100, description="Gig title")
    description: str = Field(..., min_length=20, max_length=500, description="Gig description")
    category: str = Field(..., description="Gig category")
    budget: float = Field(..., gt=0, description="Gig budget")
    client_name: str = Field(..., min_length=2, max_length=50, description="Client name")
    
    @validator('category')
    def validate_category(cls, v):
        """Ensure category is from the allowed list"""
        if v not in CATEGORIES:
            raise ValueError(f'Category must be one of: {", ".join(CATEGORIES)}')
        return v

class GigUpdate(BaseModel):
    """Model for updating an existing gig"""
    budget: Optional[float] = Field(None, gt=0, description="Updated budget")
    status: Optional[str] = Field(None, description="Updated status")
    
    @validator('status')
    def validate_status(cls, v):
        """Ensure status is valid"""
        if v is not None and v not in ["Open", "In Progress", "Closed"]:
            raise ValueError('Status must be one of: Open, In Progress, Closed')
        return v

# ============================================
# STEP 6: API ENDPOINTS
# ============================================

@app.get("/")
def root():
    """Root endpoint - API information"""
    return {
        "message": "Welcome to GigHub API",
        "admission_number": ADMISSION_NUMBER,
        "total_gigs": len(gigs_db),
        "categories": CATEGORIES,
        "currency": CURRENCY
    }

@app.get("/gigs")
def get_gigs(
    category: Optional[str] = Query(None, description="Filter by category"),
    min_budget: Optional[float] = Query(None, ge=0, description="Minimum budget"),
    max_budget: Optional[float] = Query(None, ge=0, description="Maximum budget"),
    skip: int = Query(0, ge=0, description="Number of gigs to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of gigs to return")
):
    """
    Retrieve all gigs with optional filtering and pagination.
    """
    results = gigs_db.copy()
    
    # Filter by category
    if category:
        results = [g for g in results if g["category"].lower() == category.lower()]
    
    # Filter by min budget
    if min_budget is not None:
        results = [g for g in results if g["budget"] >= min_budget]
    
    # Filter by max budget
    if max_budget is not None:
        results = [g for g in results if g["budget"] <= max_budget]
    
    # Apply pagination
    total = len(results)
    results = results[skip:skip + limit]
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "gigs": results
    }

@app.get("/gigs/{gig_id}")
def get_gig(gig_id: int):
    """
    Retrieve a single gig by its ID.
    """
    for gig in gigs_db:
        if gig["id"] == gig_id:
            return gig
    
    raise HTTPException(status_code=404, detail="Gig not found")

@app.get("/gigs/search")
def search_gigs(q: str):
    """
    Search for gigs by title (case-insensitive).
    """
    results = []
    for gig in gigs_db:
        if q.lower() in gig["title"].lower():
            results.append(gig)
    
    if not results:
        return {"message": "No gigs found matching your search", "results": []}
    
    return {"results": results}

@app.post("/gigs")
def create_gig(gig: GigCreate):
    """
    Create a new gig.
    """
    # Check for duplicate title
    for existing_gig in gigs_db:
        if existing_gig["title"].lower() == gig.title.lower():
            raise HTTPException(
                status_code=400,
                detail="A gig with this title already exists"
            )
    
    # Generate new ID
    new_id = max([g["id"] for g in gigs_db]) + 1 if gigs_db else 1
    
    # Create the new gig
    new_gig = {
        "id": new_id,
        "title": gig.title,
        "description": gig.description,
        "category": gig.category,
        "budget": gig.budget,
        "currency": CURRENCY,
        "status": "Open",
        "client_name": gig.client_name
    }
    
    gigs_db.append(new_gig)
    
    return {
        "message": "Gig created successfully",
        "gig": new_gig
    }

@app.put("/gigs/{gig_id}")
def update_gig(gig_id: int, gig_update: GigUpdate):
    """
    Update a gig's budget or status.
    """
    for index, gig in enumerate(gigs_db):
        if gig["id"] == gig_id:
            # Update fields if provided
            if gig_update.budget is not None:
                gigs_db[index]["budget"] = gig_update.budget
            
            if gig_update.status is not None:
                gigs_db[index]["status"] = gig_update.status
            
            return {
                "message": "Gig updated successfully",
                "gig": gigs_db[index]
            }
    
    raise HTTPException(status_code=404, detail="Gig not found")

@app.delete("/gigs/{gig_id}")
def delete_gig(gig_id: int):
    """
    Delete a gig from the inventory.
    """
    for index, gig in enumerate(gigs_db):
        if gig["id"] == gig_id:
            deleted_gig = gigs_db.pop(index)
            return {
                "message": "Gig deleted successfully",
                "gig": deleted_gig
            }
    
    raise HTTPException(status_code=404, detail="Gig not found")

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "total_gigs": len(gigs_db)
    }

# ============================================
# STEP 7: RUN THE APPLICATION
# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
