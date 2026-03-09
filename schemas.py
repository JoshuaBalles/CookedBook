from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Union
from enum import Enum


class RecipeCategory(str, Enum):
    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    DINNER = "Dinner"
    DESSERT = "Dessert"
    SNACK = "Snack"


class Ingredient(BaseModel):
    """Structured ingredient schema with quantity, unit, name, and notes."""
    quantity: float = Field(default=0, ge=0)
    unit: str = ""
    name: str = ""
    notes: str = ""

    @model_validator(mode='after')
    def validate_ingredient(self):
        """Validate ingredient fields."""
        if self.quantity is not None and self.quantity < 0:
            raise ValueError('Quantity cannot be negative')
        return self


class RecipeBase(BaseModel):
    """Base recipe schema with common fields."""
    title: str
    ingredients: List[Union[str, Ingredient]] = []
    instructions: List[str] = []
    cooking_time: int = Field(default=0, ge=0)
    servings: int = Field(default=1, ge=1)
    category: RecipeCategory = RecipeCategory.DINNER


class RecipeCreate(RecipeBase):
    """Schema for creating a recipe."""
    pass


class RecipeUpdate(BaseModel):
    """Schema for updating a recipe - all fields optional."""
    title: Optional[str] = None
    ingredients: Optional[List[Union[str, Ingredient]]] = None
    instructions: Optional[List[str]] = None
    cooking_time: Optional[int] = None
    servings: Optional[int] = None
    category: Optional[RecipeCategory] = None


class RecipeResponse(RecipeBase):
    """Schema for recipe response."""
    id: int
    original_servings: Optional[int] = None

    class Config:
        from_attributes = True
