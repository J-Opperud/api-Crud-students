from sqlalchemy import select
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.student import Student
from sqlalchemy.exc import IntegrityError
from app.schemas.student import StudentPatch,StudentUpdate
from app.schemas.student import StudentCreate,StudentResponse
from fastapi import APIRouter, Depends, HTTPException,status,Response


router = APIRouter(
    prefix="/students",
    tags=['students']
    )

def get_student_or_404(student_id: int, db: Session,) -> Student:
    """Helper function """

    student = db.get(Student, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
            )
    return student

#------------------CRUD Lifecycle---------------------

@router.post(
    "/students",
    response_model=StudentResponse, status_code=201)
def Create_student(
    student_data: StudentCreate, 
    db:Session = Depends(
        get_db),
        ):
    student = Student(
        **student_data.model_dump()
        )
    db.add(student)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="A student withthis email already exists"
            )
    db.refresh(student)

    return student

#----------------------multiple student list ---------------------
    
@router.get(
    "/students",
    response_model=list[StudentResponse],
    )
def get_students(
    grade_level: int | None = None, 
    is_enrolled: bool | None = None,
    db: Session = Depends(
        get_db),
    ):
    statement = select(Student)

    if grade_level is not None:
        statement = statement.where(
            Student.grade_level == grade_level
            )
    if is_enrolled is not None:
        statement = statement.where(
            Student.is_enrolled == is_enrolled
            )

    Students = db.scalars(statement).all()

    return Students


#-----------------------------single student by id ---------------------------


@router.get(
    "/students/{student_id}",
    response_model=StudentResponse,
    )
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    ):
    return get_student_or_404(student_id, db)



#---------------------------------full replacement-----------------------------


@router.put(
    "/students/{student_id}",
    response_model=StudentResponse,
    )
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
    ):

    student = get_student_or_404(student_id, db)

    student.name = student_data.name
    student.email = student_data.email
    student.grade_level = student_data.grade_level
    student.gpa = student_data.gpa
    student.is_enrolled = student_data.is_enrolled


    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A student with this email addres already exists"
            )
    db.refresh(student)

    return student



#-------------------------------------partial update-------------------------


@router.patch(
    "/students/{student_id}",
    response_model=StudentResponse,
    )
def patch_student(
    student_id: int,
    student_data: StudentPatch,
    db: Session = Depends(
        get_db),
    ):

    student = get_student_or_404(student_id, db)

    update_data = student_data.model_dump(
        exclude_unset=True
        )
#----------------------------------- user input handling-------------------
    for field, value in update_data.items():
        setattr(student, field, value)
#--------------------------------------------------------------------
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A student with this email already exists",
            )

    db.refresh(student)

    return student



@router.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    )
def delete_student(
    student_id: int,
    db: Session = Depends(
        get_db),
        ):

    student = get_student_or_404(student_id, db)

    db.delete(student)

    db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
        )
