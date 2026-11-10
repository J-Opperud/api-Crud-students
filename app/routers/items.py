
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemResponse


router = APIRouter(
    prefix="/items",
    tags=["Items"],
)


@router.get("", response_model=list[ItemResponse])
def get_items(db: Session = Depends(get_db)):
    """
    Retrieve all items.

    The SQLAlchemy select() statement uses parameterized SQL.
    """

    # SQL injection example — vulnerable:
    # query = text(f"SELECT * FROM items WHERE name = '{name}'")
    #
    # Safe approach — parameterized query:
    # query = select(Item).where(Item.name == name)
    #
    # SQLAlchemy binds values separately from SQL syntax.
    # This prevents user input from being interpreted as SQL commands.

    statement = select(Item)
    return db.scalars(statement).all()


@router.post(
    "",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_item(
    item_data: ItemCreate,
    db: Session = Depends(get_db),
):
    """Create an item using validated and sanitized input."""

    item = Item(**item_data.model_dump())

    db.add(item)
    db.commit()
    db.refresh(item)

    return item
