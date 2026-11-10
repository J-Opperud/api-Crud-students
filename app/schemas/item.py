
import re

from pydantic import BaseModel, ConfigDict, Field, field_validator


_SCRIPT_STYLE_PATTERN = re.compile(
    r"<(script|style)\b[^>]*>.*?</\1\s*>",
    re.IGNORECASE | re.DOTALL,
)

_TAG_PATTERN = re.compile(r"<[^>]+>")


class ItemCreate(BaseModel):
    """Validate and sanitize incoming item data."""

    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=2000)

    @field_validator("name", "description", mode="before")
    @classmethod
    def sanitize_text(cls, value):
        if value is None:
            return None

        if not isinstance(value, str):
            return value

        value = _SCRIPT_STYLE_PATTERN.sub("", value)
        value = _TAG_PATTERN.sub("", value)

        return value.strip()


class ItemResponse(BaseModel):
    """Schema for returning an item from the API."""

    id: int
    name: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)
