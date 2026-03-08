from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class RecipeCategory(str, Enum):
    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    DINNER = "Dinner"
    DESSERT = "Dessert"
    SNACK = "Snack"


class RecipeBase(BaseModel):
    """Base recipe schema with common fields."""
    title: str
    ingredients: List[str] = []
    instructions: List[str] = []
    cooking_time: int = 0  # In minutes
    servings: int = 1
    category: RecipeCategory = RecipeCategory.DINNER


class RecipeCreate(RecipeBase):
    """Schema for creating a recipe."""
    pass


class RecipeUpdate(BaseModel):
    """Schema for updating a recipe - all fields optional."""
    title: Optional[str] = None
    ingredients: Optional[List[str]] = None
    instructions: Optional[List[str]] = None
    cooking_time: Optional[int] = None
    servings: Optional[int] = None
    category: Optional[RecipeCategory] = None


class RecipeResponse(RecipeBase):
    """Schema for recipe response."""
    id: int

    class Config:
        from_attributes = True
