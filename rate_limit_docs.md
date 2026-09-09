API Hardening

The API was hardened with several security protections.

CORS

CORS middleware was added to app/main.py.

Only these frontend origins are allowed:

http://localhost:8501 — Streamlit frontend
http://localhost:3000 — React frontend

The allowed HTTP methods are restricted to the methods used by the API:

GET
POST
PUT
PATCH
DELETE

The allowed headers are restricted to Authorization and Content-Type.

Rate Limiting

slowapi was added to the application to limit repeated requests.

The following limits are configured:

Login: 5 requests per minute
Create student (POST): 20 requests per minute
Student list/detail GET requests: 60 requests per minute

When a client exceeds a configured limit, the API returns:

HTTP 429 Too Many Requests


with a JSON response explaining that the rate limit has been exceeded.

The rate limiter is stored in app/utils/rate_limit.py so it can be imported by the individual routers.

Input Validation

Pydantic schemas were updated with input constraints.

Student fields now have appropriate limits:

Student names: maximum 70 characters
Email addresses: maximum 250 characters
Grade level: 1–12
GPA: 0.0–4.0

Authentication schemas already contained validation for:

User name length
Valid email addresses
Password length

These constraints prevent unreasonable or malformed input from reaching the application logic.

Testing

The existing test suite was run after the security changes:

11 passed


The login rate limiter was also manually tested by making six rapid login requests. The first five requests were accepted and the sixth returned:

200 OK
200 OK
200 OK
200 OK
429 Too Many Requests


This provides evidence that the login rate limiting is functioning as required.