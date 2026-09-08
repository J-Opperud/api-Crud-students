from fastapi import APIRouter, Depends,status,Response,Query, BackgroundTasks
from sqlalchemy import select
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.utils.security import get_current_user
from app.models.student import Student
from app.schemas.student import StudentCreate,StudentResponse
from app.schemas.student import StudentPatch,StudentUpdate
from app.utils.exceptions import BadRequestException, DuplicateException, NotFoundException
from app.utils.notifications import log_activity, send_notification
from app.models.auth_user import Auth_User

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
    response_model=StudentResponse, status_code=201)
def Create_student(
    student_data: StudentCreate, 
    background_tasks: BackgroundTasks,
    current_user: Auth_User = Depends( get_current_user),
    db:Session = Depends(
        get_db),
    _: object = Depends(
        get_current_user),
        ):
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
    )
def get_students(
    grade_level: int | None = Query(
        default=None,
        ge=1,
        le=12,
    ), 
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
    "/{student_id}",
    response_model=StudentResponse,
    )
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    _:object = Depends(get_current_user),
    ):
    return get_student_or_404(student_id, db)



#-------------------full replacement-----------------------------


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
    )
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
    _:object = Depends(get_current_user),
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
    )
def patch_student(
    student_id: int,
    student_data: StudentPatch,
    db: Session = Depends(
        get_db),
    _:object = Depends(
        get_current_user),
    ):

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
    )
def delete_student(
    student_id: int,
    background_tasks: BackgroundTasks,
    current_user: Auth_User = Depends( get_current_user),
    db: Session = Depends(
        get_db),
    _:object = Depends(
        get_current_user),
        ):

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
        f"Deleted student {student.name} {student_id}")

    background_tasks.add_task(
        send_notification,
        current_user.email,
    
        f"Student {student.name} was removed successfully"
        )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT
        )
