from fastapi.testclient import TestClient

from app.main import app
from app.utils.exceptions import NotFoundException, DuplicateException, BadRequestException


client = TestClient(app)


# Temporary route used to test the exception handler
@app.get("/test-not-found")
def trigger_not_found():
    raise NotFoundException("Student", 999)


#Pytest test
def test_not_found_handler():
    response = client.get("/test-not-found")

    assert response.status_code == 404

    assert response.json() == {
        "error": "not_found",
        "detail": "Student with id 999 not found",
    }

@app.get("/test-duplicate")
def trigger_duplicate():
    raise DuplicateException(
        "Student",
        "email",
        "test@example.com",
   )

def test_duplicate_handler():
    response = client.get("/test-duplicate")

    assert response.status_code == 409

    assert response.json() == {
        "error": "duplicate",
        "detail": "Student with email 'test@example.com' already exists",
    }

@app.get("/test-bad-request")
def trigger_bad_request():
    raise BadRequestException(
        "An enrolled student cannot be deleted"
    )

def test_bad_request_handler():
    response = client.get("/test-bad-request")

    assert response.status_code == 400

    assert response.json() == {
        "error": "bad_request",
        "detail": "An enrolled student cannot be deleted",
    }
