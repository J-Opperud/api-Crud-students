from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field



class StudentCreate(BaseModel):
    name: str = Field(max_length=70)
    email: str = Field(max_length=250)
    grade_level: int = Field(ge=1, le=12)
    gpa: float | None = Field(default=None, ge=0.0, le=4.0)
    is_enrolled: bool= True




class StudentUpdate(BaseModel):
    name: str = Field(max_length=70)
    email: str = Field(max_length=250)
    grade_level: int = Field(ge=1, le=12)
    gpa: float | None = Field(default=None, ge=0.0, le=4.0)
    is_enrolled: bool




class StudentPatch(BaseModel):
    name: str | None = Field(
        default=None, 
        max_length=70,
        )
    email: str | None = Field(
        default=None, 
        max_length=250,
        )
    grade_level: int  | None = Field(
        default=None,
        ge=1, 
        le=12,
        )
    gpa: float | None = Field(
        default=None,
        ge=0.0,
        le=4.0,
        )
    is_enrolled: bool | None = None



class StudentResponse(BaseModel):
    id: int
    name: str = Field(max_length=70)
    email: str = Field(max_length=250)
    grade_level: int = Field(ge=1, le=12)
    gpa: float | None = Field(
        default=None, 
        ge=0.0, 
        le=4.0,
        )
    is_enrolled: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Jane Smith",
                "email": "jane@example.com",
                "grade_level": 11,
                "gpa": 3.8,
                "is_enrolled": True,
                "created_at": "2026-09-10T14:30:00"
            }
        }
    )
                              



