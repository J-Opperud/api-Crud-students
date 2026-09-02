from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field



class StudentCreate(BaseModel):
    name: str
    email: str
    grade_level: int = Field(ge=1, le=12)
    gpa: float | None = None
    is_enrolled: bool= True




class StudentUpdate(BaseModel):
    name: str
    email: str
    grade_level: int = Field(ge=1, le=12)
    gpa: float | None = None
    is_enrolled: bool




class StudentPatch(BaseModel):
    name: str | None = None
    email: str | None = None
    grade_level: int  | None = Field(
        default=None,
        ge=1, le=12
        )
    gpa: float | None = None
    is_enrolled: bool | None = None



class StudentResponse(BaseModel):
    name: str
    email: str
    grade_level: int
    gpa: float | None 
    is_enrolled: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



