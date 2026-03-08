import json
from typing import List
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Recipe
from schemas import RecipeCreate, RecipeUpdate, RecipeResponse

# Create FastAPI app
app = FastAPI(title="CookedBook")

# Setup templates
templates = Jinja2Templates(directory="templates")


# Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Helper functions to convert between JSON string and list
def ingredients_to_json(ingredients: List[str]) -> str:
    return json.dumps(ingredients)


def json_to_ingredients(json_str: str) -> List[str]:
    if not json_str:
        return []
    return json.loads(json_str)


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
            "instructions": json_to_ingredients(recipe.instructions),
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
def view_recipe(request: Request, recipe_id: int, session: Session = Depends(get_session)):
    """View single recipe."""
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    recipe_data = {
        "id": recipe.id,
        "title": recipe.title,
        "ingredients": json_to_ingredients(recipe.ingredients),
        "instructions": json_to_ingredients(recipe.instructions),
        "cooking_time": recipe.cooking_time,
        "servings": recipe.servings,
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
        "instructions": json_to_ingredients(recipe.instructions),
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
        instructions=ingredients_to_json(recipe.instructions),
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
        instructions=json_to_ingredients(db_recipe.instructions),
        cooking_time=db_recipe.cooking_time,
        servings=db_recipe.servings,
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
            instructions=json_to_ingredients(r.instructions),
            cooking_time=r.cooking_time,
            servings=r.servings,
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
        instructions=json_to_ingredients(recipe.instructions),
        cooking_time=recipe.cooking_time,
        servings=recipe.servings,
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
        recipe.instructions = ingredients_to_json(update_data.pop("instructions"))
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
        instructions=json_to_ingredients(recipe.instructions),
        cooking_time=recipe.cooking_time,
        servings=recipe.servings,
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
