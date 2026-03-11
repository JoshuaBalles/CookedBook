from sqlmodel import SQLModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime, timezone


class RecipeCategory(str, Enum):
    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    DINNER = "Dinner"
    DESSERT = "Dessert"
    SNACK = "Snack"


class Recipe(SQLModel, table=True):
    """Recipe database model."""
    
    __tablename__ = "recipes"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, nullable=False)
    ingredients: str = Field(default="")  # Stored as JSON string
    instructions: str = Field(default="")  # Stored as JSON string
    cooking_time: int = Field(default=0)  # In minutes
    servings: int = Field(default=1)
    category: str = Field(default=RecipeCategory.DINNER.value)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
