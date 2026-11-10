from app.main import app
from app.database import get_db, Base
from app.models.auth_user import Auth_User
from app.utils.security import hash_password
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.utils.security import get_current_user

from app.utils.rate_limit import limiter


#-------------------- Rate limiting --------------------

def test_login_rate_limit(client, test_user):
    login_data = {
        "email": "security@example.com",
        "password": "TestPassword123",
    }

    responses = []

    for _ in range(6):
        response = client.post(
            "/auth/login",
            json=login_data,
        )
        responses.append(response.status_code)

    assert responses[:5] == [200, 200, 200, 200, 200]
    assert responses[5] == 429

#------------------- Input validation --------------------

def test_student_rejects_invalid_grade(client):
    student = {
        "name": "Test Student",
        "email": "invalid-grade@example.com",
        "grade_level": 13,
        "gpa": 3.5,
        "is_enrolled": True,
        }

    response = client.post(
        "/students",
        json=student,
    )

    assert response.status_code == 422


def test_student_rejects_invalid_gpa(client):
    student = {
        "name": "Test Student",
        "email": "invalid-gpa@example.com",
        "grade_level": 10,
        "gpa": 5.0,
        "is_enrolled": True,
        }

    response = client.post(
        "/students",
        json=student,
    )

    assert response.status_code == 422


def test_student_rejects_long_name(client):
    student = {
        "name": "A" * 71,
        "email": "long-name@example.com",
        "grade_level": 10,
        "gpa": 3.5,
        "is_enrolled": True,
        }

    response = client.post(
        "/students",
        json=student,
    )

    assert response.status_code == 422


def test_login_rate_limit(client, test_user):
    # Arrange
    limiter.reset()

    login_data = {
        "email": "security@example.com",
        "password": "TestPassword123",
    }

    responses = []

    # Act
    for _ in range(11):
        response = client.post(
            "/auth/login",
            json=login_data,
        )
        responses.append(response.status_code)

    # Assert
    assert responses[:10] == [200] * 10
    assert responses[10] == 429


def test_item_strips_html_tags(client):
    # Arrange
    item = {
        "name": "<script>alert('xss')</script>Test Item",
        "description": "<b>Important</b> description",
    }

    # Act
    response = client.post("/items", json=item)

    # Assert
    assert response.status_code == 201

    data = response.json()

    assert "<script>" not in data["name"]
    assert "alert('xss')" not in data["name"]
    assert "<b>" not in data["description"]
    assert data["name"] == "Test Item"
    assert data["description"] == "Important description"

