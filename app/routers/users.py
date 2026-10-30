from fastapi import APIRouter, Depends

from app.models.auth_user import Auth_User
from app.schemas.auth import UserResponse
from app.utils.security import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    responses={
        401: {"description": "Authentication credentials are missing or invalid."},
        },
    )

def get_me(
    current_user: Auth_User = Depends(
        get_current_user),
    ):
    """
    
    Retrieve the currently authenticated user.

    - Requires valid authentication credentials.
    - Returns the authenticated user's ID, name, and email.
    - Returns 401 when authentication credentials are missing or invalid.
    
    """

    return {
        "id": current_user.id,
        "name": current_user.users_name,
        "email": current_user.email,
        }