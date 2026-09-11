from fastapi import APIRouter, Depends,status,Response,Query, BackgroundTasks, Request
from sqlalchemy import select
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.utils.security import get_current_user
from app.models.student import Student
from app.schemas.student import StudentCreate,StudentResponse
from app.schemas.student import StudentPatch,StudentUpdate
from app.models.auth_user import Auth_User
from app.utils.rate_limit import limiter
from app.utils.exceptions import BadRequestException, DuplicateException, NotFoundException
from app.utils.notifications import log_activity, send_notification

router = APIRouter(
    prefix="/students",
    tags=['students']
    )

def get_student_or_404(student_id: int, db: Session,) -> Student:
    """Helper function """

    student = db.get(Student, student_id)

    if student is None:
        raise NotFoundException(
            "Student",
            student_id,
            )
    return student

#------------------CRUD Lifecycle---------------------

@router.post(
    "",
    response_model=StudentResponse, status_code=201,
    summary="Create a student",
    responses={
        401: {"description": "Authentication credentials are missing or invalid."},
        422: {"description": "Validation error for the student data."},
        }
    )
@limiter.limit("20/minute")
def Create_student(
    request: Request,
    student_data: StudentCreate, 
    background_tasks: BackgroundTasks,
    current_user: Auth_User = Depends(get_current_user),
    db:Session = Depends(
        get_db),
        ):
    """
    Create a new student record.

    - Requires an authenticated user.
    - Validates the student data before creation.
    - Returns the newly created student.
    - Returns 422 when the student data fails validation.
    
    """

    student = Student(
        **student_data.model_dump()
        )
    db.add(student)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()

        raise DuplicateException(
            "Student",
            "email",
            student.email,
            )
            
    db.refresh(student)

    background_tasks.add_task(
        log_activity,
        current_user.email,

        f"Created student {student.name}{student.id}"
        )
    background_tasks.add_task(
        send_notification,
        current_user.email,
    
        f"Student {student.name} was created successfully"
        )


    return student

#----------------------multiple student list ---------------------
    
@router.get(
    "",
    response_model=list[StudentResponse],
    summary="List students",
    responses={
        422: {"description": "Validation error for the query parameters."},
        },
    )
@limiter.limit("60/minute")
def get_students(
    request: Request,
    grade_level: int | None = Query(
        default=None,
        ge=1,
        le=12,
    ), 
    is_enrolled: bool | None = None,
    db: Session = Depends(
        get_db),
    ):
    """

    Retrieve a list of students.

    - Returns all students when no filters are provided.
    - Supports filtering by grade level.
    - Supports filtering by enrollment status.
    - Returns 422 when a query parameter fails validation

    """
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
    "/{student_id}",
    response_model=StudentResponse,
     summary="Get a student by ID",
    responses={
        401: {"description": "Authentication credentials are missing or invalid."},
        404: {"description": "Student with the specified ID was not found."},
        422: {"description": "Validation error for the student ID."},
        },
    )
    
@limiter.limit("60/minute")
def get_student(
    request: Request,
    student_id: int,
    db: Session = Depends(get_db),
    _:object = Depends(get_current_user),
    ):
    """
    
    Retrieve a student by ID.

    - Requires an authenticated user.
    - Returns the student matching the specified ID.
    - Returns 404 when the student does not exist.
    - Returns 422 when the student ID is invalid.
    
    """
    return get_student_or_404(student_id, db)



#-------------------full replacement-----------------------------


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Update a student",
    responses={
        401: {"description": "Authentication credentials are missing or invalid."},
        404: {"description": "Student with the specified ID was not found."},
        422: {"description": "Validation error for the student ID or student data."},
        },
    )

def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
    _:object = Depends(get_current_user),
    ):

    """
    Update an existing student.

    - Requires an authenticated user.
    - Replaces all the student's current information with the provided data.
    - Returns the updated student.
    - Returns 404 when the student does not exist.
    - Returns 422 when the request data is invalid.
    
    """

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
        raise DuplicateException(
            "Student",
            "email",
            student.email,
            )
    db.refresh(student)

    return student



#-------------------------------------partial update-------------------------


@router.patch(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Partially update a student",
    responses={
        400: {"description": "At least one field must be provided."},
        401: {"description": "Authentication credentials are missing or invalid."},
        404: {"description": "Student with the specified ID was not found."},
        422: {"description": "Validation error for the student ID or update data."},
        },
    )
def patch_student(
    student_id: int,
    student_data: StudentPatch,
    db: Session = Depends(
        get_db),
    _:object = Depends(
        get_current_user),
    ):
    """
    
    Partially update an existing student.

    - Requires an authenticated user.
    - Updates only the fields provided in the request.
    - Returns the updated student.
    - Returns 400 when no fields are provided.
    - Returns 404 when the student does not exist.
    - Returns 422 when the request data is invalid.
    
    """
     
    student = get_student_or_404(student_id, db)

    update_data = student_data.model_dump(
        exclude_unset=True
        )
#----------------------- user input handling-------------------
    for field, value in update_data.items():
        setattr(student, field, value)
#-----------------------Empty field handling
    if not update_data:
        raise BadRequestException(
            "At least one field must be provided"
            )

#--------------------------------------------------------------------
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateException(
            "Student",
            "email",
            student.email,
            )

    db.refresh(student)

    return student



@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
     summary="Delete a student",
    responses={
        400: {"description": "An enrolled student cannot be deleted."},
        401: {"description": "Authentication credentials are missing or invalid."},
        404: {"description": "Student with the specified ID was not found."},
        422: {"description": "Validation error for the student ID."},
        },
    )

def delete_student(
    student_id: int,
    background_tasks: BackgroundTasks,
    current_user: Auth_User = Depends(
        get_current_user),
    db: Session = Depends(
        get_db),
        ):

    """
    
    Delete a student by ID.

    - Requires an authenticated user.
    - Deletes the student when the student is not enrolled.
    - Returns 400 when an enrolled student cannot be deleted.
    - Returns 404 when the student does not exist.
    - Returns 204 after successful deletion.
    
    """

    student = get_student_or_404(student_id, db)
    if student.is_enrolled:
        raise BadRequestException(
            "An enrolled student cannot be deleted"
        )

    db.delete(student)

    db.commit()

    background_tasks.add_task(
        log_activity, 
        current_user.email,
        f"Deleted student {student.name} {student_id}"
        )

    background_tasks.add_task(
        send_notification,
        current_user.email,
    
        f"Student {student.name} was removed successfully"
        )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT
        )
