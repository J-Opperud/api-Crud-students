Student Database API

## Objective

A FastAPI  implementing full CRUD operations for a Student resource using SQLAlchemy and SQLite.

Project Structure

api-student/
│
├── app/
│   ├── main.py
│   ├── database.py
│   │
│   ├── models/
│   │   └── student.py
│   │
│   ├── schemas/
│   │   └── student.py
│   │
│   ├── routers/
│   │   └── students.py
│   │
│   └── utils/
│       └── exceptions.py
│
├── tests/
│   ├── test_lab.py
│   └── test_lab2.py
│
├── requirements.txt
└── README.md

## Design Notes

The application separates responsibilities between the API, validation, database models, and persistence layers:

FastAPI
   ↓
Pydantic Schemas
   ↓
SQLAlchemy Models
   ↓
SQLite Database

Custom exceptions are handled globally by FastAPI:

Application Error
      ↓
Custom Exception
      ↓
Global Exception Handler
      ↓
Consistent JSON Response

## Build and demonstrate CRUD pattern:

    Create students
    Retrieve students individually or as a collection
    Filter students by grade level and enrollment status
    Fully replace a student with PUT
    Partially update a student with PATCH
    Delete a student

## Tech Stack

    FastAPI — API framework and automatic Swagger documentation
    Pydantic — request and response validation
    SQLAlchemy — ORM and database interaction
    SQLite — lightweight database for development and testing
    pytest — automated testing framework
    FastAPI TestClient — endpoint testing without running the server separately

## Student Model

The Student database model contains:
- Field, Type, Description
- id, Integer, Primary key
- name, String,	Required
- email, String, Required and unique
- grade_level, Integer	1–12
- gpa, Float, Optional
- is_enrolled, Boolean, Defaults to True
- created_at, DateTime, Automatically generated
API Endpoints
- Method Endpoint Purpose
- POST	/students Create a student
- GET	/students List students
- GET	/students/{id} Get one student
- PUT	/students/{id} Full replacement
- PATCH	/students/{id} Partial update
- DELETE	/students/{id} Delete a student
- Filtering

GET /students supports:

/students?grade_level=10
/students?is_enrolled=true
/students?grade_level=10&is_enrolled=true

## Request Schemas

    StudentCreate — used when creating a student.
    StudentUpdate — requires the complete student representation for PUT.
    StudentPatch — all fields are optional for partial updates.
    StudentResponse — defines the data returned by the API.

Pydantic validates constraints such as grade_level being between 1 and 12.

## Error Handling

Custom Error Handling

The application uses custom exceptions instead of raising HTTPException directly from the CRUD router.
Custom Exceptions

    NotFoundException — resource does not exist.
    DuplicateException — unique constraint violation.
    BadRequestException — invalid business logic.

These exceptions are registered with global handlers in main.py so that errors have a consistent response format.
Error Responses
404 — Student Not Found

{
  "error": "not_found",
  "detail": "Student with id 999 not found"
}

409 — Duplicate Email

{
  "error": "duplicate",
  "detail": "Student with email 'student@example.com' already exists"
}

400 — Invalid Business Logic

An enrolled student cannot be deleted.

{
  "error": "bad_request",
  "detail": "An enrolled student cannot be deleted"
}

Database IntegrityError exceptions are rolled back before raising the appropriate custom exception.
Helper Function
Setup

## Install dependencies:

pip install -r requirements.txt

## Run the application:

uvicorn app.main:app --reload

Open Swagger UI:

http://127.0.0.1:8000/docs

4. Run Automated Tests

From the project root:

python -m pytest -v

CRUD Test Cycle

 tested sequence is:

POST
 ↓
GET collection
 ↓
GET by ID
 ↓
PUT
 ↓
PATCH
 ↓
DELETE
 ↓
GET by ID → 404

 testing the important edge cases:

    




