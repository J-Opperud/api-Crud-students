from app.database import get_db
from sqlalchemy.orm import Session
from app.models.auth_user import Auth_User
from app.utils.exceptions import DuplicateException
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse,UserResponse
from app.utils.security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
    )


@router.post(
    "/register", 
    response_model=TokenResponse, 
    status_code=201
    )
def register(
    request: RegisterRequest, 
    db: Session = Depends(
        get_db)
    ):
    """Register a new user return token."""

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
        response_model=TokenResponse
        )
def login(
    request: LoginRequest, 
    db: Session = Depends(
    get_db)
    ):
    """Log in and recive a access token."""
    user = db.query(Auth_User).filter(Auth_User.email == request.email).first()

    if not user or not verify_password(request.password, user.hashed_password):
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



    