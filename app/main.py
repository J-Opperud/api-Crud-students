"""
Security measures:

- CORS restricted to localhost:8501 (Streamlit)
  and localhost:3000 (React).
- CORS methods restricted to methods used by the API.
- Rate limiting implemented with slowapi.
- Login endpoint limited to 5 requests per minute.
- POST/create endpoints limited to 20 requests per minute.
- GET/list/detail endpoints limited to 60 requests per minute.
- Pydantic schemas enforce string length limits.
- Pydantic schemas enforce reasonable numeric bounds.
- Rate-limit violations return HTTP 429 Too Many Requests.
"""

from app.routers import users, auth_rout, students
from fastapi import FastAPI,Request
from app.database import Base, engine
from app.models.auth_user import Auth_User
from fastapi.responses import JSONResponse
from app.utils.exceptions import (BadRequestException,DuplicateException,NotFoundException)


from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from app.utils.rate_limit import limiter



app = FastAPI(
    title="Student API",
    description="A FastAPI application for managing Students with SQLite.",
    )

#--------------------security: Rate limit------
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(
    request: Request, 
    exc: RateLimitExceeded,
    ):
    return JSONResponse(
        status_code=429,
        content={
            "error": "rate_limit_exceeded",
            "detail": "Too many requests. Please try again later"
            }
    )
@app.exception_handler(NotFoundException)
async def not_found_handler(
    request: Request,
    exc: NotFoundException,
    ):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "not_found",
            "detail": exc.detail,
            },
    )

@app.exception_handler(DuplicateException)
async def duplicate_handler(
    request: Request,
    exc: DuplicateException,
    ):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "duplicate",
            "detail": exc.detail,
            },
    )

#------------------Security: CORS----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://localhost:3000",
        ],
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE"
        ],
    allow_headers=["Authorization","Content-Type"],
    )
#----------------------------------------------



Base.metadata.create_all(bind=engine)


@app.exception_handler(BadRequestException)
async def bad_request_handler(
    request: Request,
    exc: BadRequestException,
    ):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "bad_request",
            "detail": exc.detail,
            },
    )
app.include_router(students.router)
app.include_router(auth_rout.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Sudents API"}
