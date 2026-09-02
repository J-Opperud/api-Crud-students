from fastapi import FastAPI

from app.database import Base, engine
from app.routers import students


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Notes API",
    description="A FastAPI application for managing Students with SQLite.",
    )



app.include_router(students.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Sudents API"}
