import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base
from app.utils.security import get_current_user, hash_password
from app.models.auth_user import Auth_User


# -------------------- Test database --------------------

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


# -------------------- Authentication --------------------

class FakeUser:
    id = 1
    email = "test@example.com"


def override_get_current_user():
    return FakeUser()


app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db


# -------------------- Fixtures --------------------

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_student():
    return {
        "name": "Sample Student",
        "email": "sample@example.com",
        "grade_level": 10,
        "gpa": 3.5,
        "is_enrolled": True,
    }


@pytest.fixture
def auth_headers():
    db = TestingSessionLocal()

    email = "fixture-user@example.com"

    existing_user = (
        db.query(Auth_User)
        .filter(Auth_User.email == email)
        .first()
    )

    if existing_user:
        user = existing_user
    else:
        user = Auth_User(
            users_name="Fixture User",
            email=email,
            hashed_password=hash_password("TestPassword123"),
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    db.close()

    response = TestClient(app).post(
        "/auth/login",
        json={
            "email": email,
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }
@pytest.fixture
def test_user():
    db = TestingSessionLocal()

    user = Auth_User(
        users_name="Security Test User",
        email="security@example.com",
        hashed_password=hash_password("TestPassword123"),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    db.close()

    return user
