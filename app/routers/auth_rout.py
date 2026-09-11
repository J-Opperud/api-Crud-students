from app.database import get_db
from sqlalchemy.orm import Session
from app.models.auth_user import Auth_User
from app.utils.exceptions import DuplicateException
from fastapi import APIRouter, Depends, HTTPException, Request
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse,UserResponse
from app.utils.security import hash_password, verify_password, create_access_token
from app.utils.rate_limit import limiter

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
    )


@router.post(
    "/register", 
    response_model=TokenResponse, 
    status_code=201,
    summary="user receives token, the password is hashed before storage.",
    responses={
        422: {"description": "Validation error for the registration data."},
        },
    )
def register(
    request: RegisterRequest, 
    db: Session = Depends(
        get_db)
    ):

    existing = db.query(Auth_User).filter(
        (Auth_User.email == request.email) |
        (Auth_User.users_name == request.name)
        ).first()


    if existing:
        raise DuplicateException(
            "users",
            "email or username",
            request.email,
            )


    user = Auth_User(
        users_name = request.name,
        email = request.email,
        hashed_password=hash_password(request.password)
        )
    db.add(user)
    db.commit()
    db.refresh(user)


    token = create_access_token(
        data={"sub": str(user.id)}
        )
    return {
        "access_token": token, 
        "token_type": "bearer"
        }
@router.post(
        "/login", 
        response_model=TokenResponse,
        summary="Log in a user",
        responses={
            422: {"description": "Validation error for the login data."},
            401: {"description": " Invalid email or password."},
            },
        )
@limiter.limit("5/minute")
def login(
    request: Request,
    login_data: LoginRequest, 
    db: Session = Depends(
    get_db)
    ):
    """
    Authenticate a user and return an access token.

    - Verifies the user's email and password.
    - Returns a bearer access token after successful authentication.
    - Returns 401 when the email or password is invalid.
    - Returns 422 when the login data fails validation."""
    
    user = db.query(Auth_User).filter(Auth_User.email == login_data.email).first()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401, 
            detail="Invalid password or email")

    token = create_access_token(
        data={"sub": str(user.id)}
        )
    return {
        "access_token": token, 
        "token_type": "bearer"
        }



    