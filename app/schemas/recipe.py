from pydantic import BaseModel
from typing import Optional


REQUIRED_FIELDS = ("title", "making_time", "serves", "ingredients", "cost")


class RecipeCreateSchema(BaseModel):
    title: str
    making_time: str
    serves: str
    ingredients: str
    cost: int

class RecipeUpdateSchema(BaseModel):

    title: Optional[str] = None
    making_time: Optional[str] = None
    serves: Optional[str] = None
    ingredients: Optional[str] = None
    cost: Optional[int] = None

    def apply_to(self, current: dict) -> dict:
        updated = current.copy()
        for field in REQUIRED_FIELDS:
            value = getattr(self, field)
            if value is not None:
                updated[field] = value
        return updated