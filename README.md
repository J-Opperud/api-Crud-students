Student Database API

## Objective

A FastAPI  implementing full CRUD operations for a Student resource using SQLAlchemy and SQLite.

## Design Notes

The application separates responsibilities:

FastAPI
   ↓
Pydantic schemas
   ↓
SQLAlchemy model
   ↓
SQLite database

## Build and demonstrate CRUD pattern:

    Create students
    Retrieve students individually or as a collection
    Filter students by grade level and enrollment status
    Fully replace a student with PUT
    Partially update a student with PATCH
    Delete a student

## Tech Stack

    FastAPI — API framework and automatic Swagger documentation
    Pydantic — request/response validation
    SQLAlchemy — ORM and database interaction
    SQLite — lightweight database for development/testing

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

    404 Not Found — requested student does not exist.
    409 Conflict — email already belongs to another student.
    204 No Content — successful deletion.

The reusable get_student_or_404() helper centralizes student lookup and 404 handling, keeping the CRUD endpoints DRY.
Setup

## Install dependencies:

pip install fastapi uvicorn sqlalchemy

## Run the application:

uvicorn app.main:app --reload

Open Swagger UI:

http://127.0.0.1:8000/docs

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

    Duplicate email → 409
    Nonexistent student → 404
    Invalid grade level → validation error
    PATCH with a single field → only that field changes


