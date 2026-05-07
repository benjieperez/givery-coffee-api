from pydantic import BaseModel
from typing import Optional


REQUIRED_FIELDS = ("title", "making_time", "serves", "ingredients", "cost")


class RecipeCreateSchema(BaseModel):
    """Payload for POST /recipes — all fields required by the spec."""

    title: Optional[str] = None
    making_time: Optional[str] = None
    serves: Optional[str] = None
    ingredients: Optional[str] = None
    cost: Optional[int] = None

    def is_valid(self) -> bool:
        """Return True only when every required field is present."""
        return all(getattr(self, f) is not None for f in REQUIRED_FIELDS)


class RecipeUpdateSchema(BaseModel):
    """Payload for PATCH /recipes/{id} — all fields optional."""

    title: Optional[str] = None
    making_time: Optional[str] = None
    serves: Optional[str] = None
    ingredients: Optional[str] = None
    cost: Optional[int] = None

    def apply_to(self, current: dict) -> dict:
        """Merge non-None patch fields onto the current recipe dict."""
        updated = current.copy()
        for field in REQUIRED_FIELDS:
            value = getattr(self, field)
            if value is not None:
                updated[field] = value
        return updated