from app.routers import users, auth_rout, students
from fastapi import FastAPI,Request
from app.database import Base, engine
from app.models.auth_user import Auth_User
from fastapi.responses import JSONResponse
from app.utils.exceptions import (BadRequestException,DuplicateException,NotFoundException)



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student API",
    description="A FastAPI application for managing Students with SQLite.",
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
