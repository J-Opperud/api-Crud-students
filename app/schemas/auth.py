from pydantic import BaseModel, ConfigDict, Field, EmailStr


class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(
        min_length=8, 
        max_length=72)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(max_length=72)



class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "example-access-token..",
                "token_type": "bearer"
                }
        }
    )

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Jane Smith",
                "email": "jane@example.com"
                }
        }
    )


