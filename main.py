import json
import re
from typing import List, Union
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Recipe
from schemas import RecipeCreate, RecipeUpdate, RecipeResponse, Ingredient

# Create FastAPI app
app = FastAPI(title="CookedBook")

# Setup templates
templates = Jinja2Templates(directory="templates")


# Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Helper functions to convert between JSON string and list
def ingredients_to_json(ingredients: List[Union[str, dict, Ingredient]]) -> str:
    """Convert ingredients list to JSON string."""
    # Convert any ingredient to dict format
    result = []
    for ing in ingredients:
        if isinstance(ing, str):
            # Legacy string format - try to parse it
            result.append(_parse_legacy_ingredient(ing))
        elif isinstance(ing, Ingredient):
            result.append(ing.model_dump())
        elif isinstance(ing, dict):
            result.append(ing)
        else:
            result.append({"quantity": 0, "unit": "", "name": str(ing), "notes": ""})
    return json.dumps(result)


def instructions_to_json(instructions: List[str]) -> str:
    """Convert instructions list to JSON string (simple strings, not structured)."""
    return json.dumps(instructions)


def _parse_legacy_ingredient(ingredient_str: str) -> dict:
    """Parse a legacy string ingredient into structured format."""
    # Common patterns: "2 cups flour", "1 tsp salt", "3 eggs", "1 1/2 cups flour"
    
    # Pattern to match quantity at the start (supports simple fractions and mixed fractions)
    quantity_pattern = r'^([\d]+[\s]+[\d]+/[\d]+|[\d]+/[\d]+|[\d]+)\s*'
    match = re.match(quantity_pattern, ingredient_str)
    
    if match:
        quantity_str = match.group(1).strip()
        try:
            if ' ' in quantity_str:  # Handle mixed fractions like "1 1/2"
                whole, frac = quantity_str.split()
                num, denom = frac.split('/')
                quantity = float(whole) + float(num) / float(denom)
            elif '/' in quantity_str:  # Handle simple fractions like "1/2"
                num, denom = quantity_str.split('/')
                quantity = float(num) / float(denom)
            else:
                quantity = float(quantity_str)
        except ValueError:
            quantity = 0
        rest = ingredient_str[match.end():].strip()
    else:
        quantity = 0
        rest = ingredient_str.strip()
    
    # Common units to detect
    units = ['cups', 'cup', 'tbsp', 'tablespoon', 'tablespoons', 'tsp', 'teaspoon',
             'teaspoons', 'oz', 'ounce', 'ounces', 'lb', 'lbs', 'pound', 'pounds',
             'g', 'gram', 'grams', 'kg', 'kilogram', 'kilograms', 'ml', 'milliliter',
             'l', 'liter', 'liters', 'each', 'pinch', 'clove', 'cloves']
    
    unit = ""
    name = rest
    
    # Check if first word is a unit
    words = rest.split()
    if words and words[0].lower() in units:
        unit = words[0]
        name = " ".join(words[1:])
    
    return {
        "quantity": quantity,
        "unit": unit,
        "name": name,
        "notes": ""
    }


def json_to_ingredients(json_str: str) -> List[dict]:
    """Convert JSON string to list of ingredient dicts."""
    if not json_str:
        return []
    try:
        ingredients = json.loads(json_str)
        # Handle both old string format and new dict format
        result = []
        for ing in ingredients:
            if isinstance(ing, str):
                result.append(_parse_legacy_ingredient(ing))
            else:
                result.append(ing)
        return result
    except json.JSONDecodeError:
        return []


def json_to_instructions(json_str: str) -> List[str]:
    """Convert JSON string to list of instruction strings."""
    if not json_str:
        return []
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return []


def scale_ingredient(ingredient: dict, scale_factor: float) -> dict:
    """Scale an ingredient by the given factor."""
    scaled = ingredient.copy()
    if 'quantity' in scaled and scaled['quantity'] is not None:
        scaled['quantity'] = scaled['quantity'] * scale_factor
    return scaled


def get_scaled_ingredients(ingredients: List[dict], original_servings: int, desired_servings: int) -> List[dict]:
    """Get ingredients scaled for desired servings."""
    if original_servings <= 0 or desired_servings <= 0:
        return ingredients
    
    scale_factor = desired_servings / original_servings
    return [scale_ingredient(ing, scale_factor) for ing in ingredients]


# HTML Routes
@app.get("/", response_class=HTMLResponse)
def home(request: Request, session: Session = Depends(get_session)):
    """Home page - list all recipes."""
    recipes = session.exec(select(Recipe)).all()
    
    # Convert JSON strings back to lists for display
    recipes_data = []
    for recipe in recipes:
        recipes_data.append({
            "id": recipe.id,
            "title": recipe.title,
            "ingredients": json_to_ingredients(recipe.ingredients),
            "instructions": json_to_instructions(recipe.instructions),
            "cooking_time": recipe.cooking_time,
            "servings": recipe.servings,
            "category": recipe.category
        })
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "recipes": recipes_data
    })


@app.get("/create", response_class=HTMLResponse)
def create_page(request: Request):
    """Create recipe page."""
    return templates.TemplateResponse("create.html", {"request": request})


@app.get("/recipes/{recipe_id}", response_class=HTMLResponse)
def view_recipe(request: Request, recipe_id: int, servings: int = None, session: Session = Depends(get_session)):
    """View single recipe with optional scaling."""
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Get base ingredients
    ingredients = json_to_ingredients(recipe.ingredients)
    
    # Apply scaling if requested (with upper bound validation)
    original_servings = recipe.servings
    if servings and servings > 0:
        display_servings = min(servings, 1000)  # Cap at 1000 servings
    else:
        display_servings = original_servings
    
    if servings and servings != original_servings:
        ingredients = get_scaled_ingredients(ingredients, original_servings, servings)
    
    recipe_data = {
        "id": recipe.id,
        "title": recipe.title,
        "ingredients": ingredients,
        "instructions": json_to_instructions(recipe.instructions),
        "cooking_time": recipe.cooking_time,
        "servings": display_servings,
        "original_servings": original_servings,
        "category": recipe.category
    }
    
    return templates.TemplateResponse("view.html", {
        "request": request,
        "recipe": recipe_data
    })


@app.get("/recipes/{recipe_id}/edit", response_class=HTMLResponse)
def edit_page(request: Request, recipe_id: int, session: Session = Depends(get_session)):
    """Edit recipe page."""
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    recipe_data = {
        "id": recipe.id,
        "title": recipe.title,
        "ingredients": json_to_ingredients(recipe.ingredients),
        "instructions": json_to_instructions(recipe.instructions),
        "cooking_time": recipe.cooking_time,
        "servings": recipe.servings,
        "category": recipe.category
    }
    
    return templates.TemplateResponse("edit.html", {
        "request": request,
        "recipe": recipe_data
    })


# API Routes (JSON)
@app.post("/api/recipes", response_model=RecipeResponse)
def create_recipe(recipe: RecipeCreate, session: Session = Depends(get_session)):
    """Create a new recipe."""
    db_recipe = Recipe(
        title=recipe.title,
        ingredients=ingredients_to_json(recipe.ingredients),
        instructions=instructions_to_json(recipe.instructions),
        cooking_time=recipe.cooking_time,
        servings=recipe.servings,
        category=recipe.category.value
    )
    session.add(db_recipe)
    session.commit()
    session.refresh(db_recipe)
    
    return RecipeResponse(
        id=db_recipe.id,
        title=db_recipe.title,
        ingredients=json_to_ingredients(db_recipe.ingredients),
        instructions=json_to_instructions(db_recipe.instructions),
        cooking_time=db_recipe.cooking_time,
        servings=db_recipe.servings,
        original_servings=db_recipe.servings,
        category=db_recipe.category
    )


@app.get("/api/recipes", response_model=List[RecipeResponse])
def list_recipes(session: Session = Depends(get_session)):
    """List all recipes."""
    recipes = session.exec(select(Recipe)).all()
    
    return [
        RecipeResponse(
            id=r.id,
            title=r.title,
            ingredients=json_to_ingredients(r.ingredients),
            instructions=json_to_instructions(r.instructions),
            cooking_time=r.cooking_time,
            servings=r.servings,
            original_servings=r.servings,
            category=r.category
        )
        for r in recipes
    ]


@app.get("/api/recipes/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int, session: Session = Depends(get_session)):
    """Get a single recipe."""
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    return RecipeResponse(
        id=recipe.id,
        title=recipe.title,
        ingredients=json_to_ingredients(recipe.ingredients),
        instructions=json_to_instructions(recipe.instructions),
        cooking_time=recipe.cooking_time,
        servings=recipe.servings,
        original_servings=recipe.servings,
        category=recipe.category
    )


@app.put("/api/recipes/{recipe_id}", response_model=RecipeResponse)
def update_recipe(recipe_id: int, recipe_update: RecipeUpdate, session: Session = Depends(get_session)):
    """Update a recipe."""
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    update_data = recipe_update.model_dump(exclude_unset=True)
    
    if "ingredients" in update_data:
        recipe.ingredients = ingredients_to_json(update_data.pop("ingredients"))
    if "instructions" in update_data:
        recipe.instructions = instructions_to_json(update_data.pop("instructions"))
    if "category" in update_data:
        update_data["category"] = update_data["category"].value
    
    for field, value in update_data.items():
        setattr(recipe, field, value)
    
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    
    return RecipeResponse(
        id=recipe.id,
        title=recipe.title,
        ingredients=json_to_ingredients(recipe.ingredients),
        instructions=json_to_instructions(recipe.instructions),
        cooking_time=recipe.cooking_time,
        servings=recipe.servings,
        original_servings=recipe.servings,
        category=recipe.category
    )


@app.delete("/api/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, session: Session = Depends(get_session)):
    """Delete a recipe."""
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    session.delete(recipe)
    session.commit()
    
    return {"message": "Recipe deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
