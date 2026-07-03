# GigHub API

## Description

GigHub API is a FastAPI application for managing freelance job listings. It allows clients to post gigs and freelancers to view available opportunities. The API supports creating, viewing, updating, deleting, and searching for gigs.

## Features


- View all gigs
- Filter gigs by category and budget
- View a gig by ID
- Search gigs by title
- Create a new gig
- Update a gig's budget or status
- Delete a gig

## Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn

## Running the API

1. Install the required packages:

```bash
pip install fastapi uvicorn
```

2. Start the server:

```bash
uvicorn main:app --reload
```

3. Open your browser and visit:

```
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically generates API documentation.

Swagger UI:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

## Author

**YVONNE MAKAU**

Admission Number: **C027-01-0860/2024**
