
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Item(Base):
    """Database model representing an item."""

    __tablename__ = "items"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
