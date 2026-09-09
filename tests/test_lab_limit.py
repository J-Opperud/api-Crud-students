from app.main import app
from app.database import get_db, Base
from app.models.auth_user import Auth_User
from app.utils.security import hash_password
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.utils.security import get_current_user

#-------------------- Test database --------------------
class FakeUser:
    id = 1
    email = "test@example.com"


def override_get_current_user():
    return FakeUser()


app.dependency_overrides[get_current_user] = override_get_current_user


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

#-------------------- Test user --------------------
def create_test_user():
    db = TestingSessionLocal()

    user = Auth_User(
        users_name="Security Test User",
        email="security@example.com",
        hashed_password=hash_password("TestPassword123"),
    )

    db.add(user)
    db.commit()
    db.close()

create_test_user()

#-------------------- Rate limiting --------------------

def test_login_rate_limit():
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

def test_student_rejects_invalid_grade():
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


def test_student_rejects_invalid_gpa():
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


def test_student_rejects_long_name():
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