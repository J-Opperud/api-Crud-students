from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base


TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)



client = TestClient(app)


def test_get_student_not_found():
    response = client.get("/students/999")

    assert response.status_code == 404

    assert response.json() == {
        "error": "not_found",
        "detail": "Student with id 999 not found",
    }


def test_duplicate_student_email():
    student = {
        "name": "John Smith",
        "email": "smiththesith@example.com",
        "grade_level": 10,
        "gpa": 3.5,
        "is_enrolled": True,
    }

    first_response = client.post("/students", json=student)

    
    print(first_response.json())

    assert first_response.status_code == 201

    duplicate_response = client.post(
        "/students",
        json=student,
    )

    assert duplicate_response.status_code == 409

    assert duplicate_response.json() == {
        "error": "duplicate",
        "detail": "Student with email 'smiththesith@example.com' already exists",
    }

def test_delete_enrolled_student():
    student = {
        "name": "Jane Doe",
        "email": "doeyes@example.com",
        "grade_level": 11,
        "gpa": 3.8,
        "is_enrolled": True,
    }

    create_response = client.post(
        "/students",
        json=student,
    )
    print(create_response.json())
    assert create_response.status_code == 201
    
    student_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/students/{student_id}"
    )

    assert delete_response.status_code == 400

    assert delete_response.json() == {
        "error": "bad_request",
        "detail": "An enrolled student cannot be deleted",
    }

def test_create_student():
    student = {
        "name": "Jackie Reacher",
        "email": "reacher@example.com",
        "grade_level": 10,
        "gpa": 3.5,
        "is_enrolled": True,
}

    response = client.post("/students", json=student)

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Jackie Reacher"
    assert data["email"] == "reacher@example.com"
    assert "id" in data

def test_get_student():
    student = {
        "name": "Chips Johnson",
        "email": "gettest@example.com",
        "grade_level": 9,
        "gpa": 3.7,
        "is_enrolled": True,
    }

    create_response = client.post("/students", json=student)

    assert create_response.status_code == 201

    student_id = create_response.json()["id"]

    response = client.get(f"/students/{student_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == student_id
    assert data["name"] == "Chips Johnson"
    assert data["email"] == "gettest@example.com"

def test_patch_student():
    student = {
        "name": "Patch Student",
        "email": "patch@example.com",
        "grade_level": 10,
        "gpa": 3.2,
        "is_enrolled": True,
    }

    create_response = client.post("/students", json=student)

    assert create_response.status_code == 201

    student_id = create_response.json()["id"]

    response = client.patch(
        f"/students/{student_id}",
        json={"gpa": 3.9},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == student_id
    assert data["gpa"] == 3.9
    assert data["name"] == "Patch Student"
    assert data["email"] == "patch@example.com"

def test_update_student():
    student = {
        "name": "Original Student",
        "email": "original@example.com",
        "grade_level": 9,
        "gpa": 3.1,
        "is_enrolled": True,
    }

    create_response = client.post("/students", json=student)

    assert create_response.status_code == 201

    student_id = create_response.json()["id"]

    updated_student = {
        "name": "Updated Student",
        "email": "updated@example.com",
        "grade_level": 12,
        "gpa": 3.9,
        "is_enrolled": False,
    }

    response = client.put(
        f"/students/{student_id}",
        json=updated_student,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == student_id
    assert data["name"] == "Updated Student"
    assert data["email"] == "updated@example.com"
    assert data["grade_level"] == 12
    assert data["gpa"] == 3.9
    assert data["is_enrolled"] is False

def test_delete_student():
    student = {
        "name": "Delete Student",
        "email": "delete@example.com",
        "grade_level": 10,
        "gpa": 3.4,
        "is_enrolled": False,
    }

    create_response = client.post("/students", json=student)

    assert create_response.status_code == 201

    student_id = create_response.json()["id"]

    response = client.delete(f"/students/{student_id}")

    assert response.status_code == 204

    assert response.content == b""
