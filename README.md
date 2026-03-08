# CookedBook
## A hobby app for cataloging personal recipes.

# CookedBook - Recipe Management App

## Tech Stack
- Backend: FastAPI (Python)
- Database: SQLite (via SQLModel)
- Frontend: Pure HTML/CSS with Jinja2 templates
- UI Theme: GitHub Dark Mode

## Project Structure
CookedBook/
├── main.py           # FastAPI app, routes, and CRUD logic
├── models.py         # SQLModel database model (Recipe table)
├── schemas.py        # Pydantic schemas for request/response
├── database.py       # SQLite engine and session setup
├── requirements.txt  # Dependencies
└── templates/        # HTML templates
    ├── index.html    # Home - list all recipes
    ├── create.html   # Form to create new recipe
    ├── view.html     # View single recipe details
    └── edit.html     # Form to edit existing recipe

## Recipe Model Fields
- id (auto-generated)
- title (string)
- ingredients (list of strings, stored as JSON)
- instructions (list of strings, stored as JSON)
- cooking_time (integer - minutes)
- servings (integer)
- category (enum: Breakfast, Lunch, Dinner, Dessert, Snack)

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Home page (HTML) |
| GET | /create | Create recipe page |
| GET | /recipes/{id} | View recipe page |
| GET | /recipes/{id}/edit | Edit recipe page |
| POST | /api/recipes | Create recipe (JSON API) |
| GET | /api/recipes | List all recipes (JSON API) |
| GET | /api/recipes/{id} | Get single recipe (JSON API) |
| PUT | /api/recipes/{id} | Update recipe (JSON API) |
| DELETE | /api/recipes/{id} | Delete recipe (JSON API)

## Running the App
```conda activate CookedBook```
```python3 -m main``` 
# Open http://localhost:8000

## Future Development Ideas
- Add recipe photos/images
- Add search and filtering
- Add ingredient scaling
- Add export to PDF
- Add meal planning features
- Add print-friendly view
- Add user authentication
- Add recipe ratings/favorites