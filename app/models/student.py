





from sqlalchemy import String, DateTime,Integer,Boolean,Float
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from sqlalchemy.sql import func

from datetime import datetime



class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(
        primary_key=True
        )
    name: Mapped[str] = mapped_column(
        String(70),
        nullable=False
        )
    email: Mapped[str] = mapped_column(
        String(250),
        unique=True,
        nullable=False
        )
    grade_level: Mapped[int] =mapped_column(
        Integer,
        nullable=False
        )
    gpa: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
        )
    is_enrolled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
        )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
        )








#     grade_level (integer, 1-12)
#     gpa (float, optional)
#     is_enrolled (boolean, default True)
    # created_at (datetime, auto-generated)