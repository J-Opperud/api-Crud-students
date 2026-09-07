from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String
from app.database import Base












class Auth_User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
        )
    users_name: Mapped[str] = mapped_column(
        String(70),
        unique=True,
        nullable=False
        )
    email: Mapped[str] = mapped_column(
        String(250),
        unique=True,
        nullable=False
        )
    hashed_password: Mapped[str] = mapped_column(
        String(250),
        
        nullable=False,
        )
    


