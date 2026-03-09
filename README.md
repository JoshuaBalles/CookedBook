# 🍳 CookedBook

A simple and elegant web application for cataloging and managing your personal recipe collection.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML/CSS](https://img.shields.io/badge/HTML%2FCSS-E34F26?style=for-the-badge&logo=html5&logoColor=white)

## 📖 About

CookedBook is a hobby project built to help you organize and store your personal recipes in one convenient place. Whether it's family favorites or experimental dishes, keep everything organized with an easy-to-use interface.

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI (Python) |
| Database | SQLite (via SQLModel) |
| Frontend | Pure HTML/CSS with Jinja2 Templates |
| UI Theme | GitHub Dark Mode |

## 📁 Project Structure

```
CookedBook/
├── main.py              # FastAPI application, routes, and CRUD logic
├── models.py            # SQLModel database model (Recipe table)
├── schemas.py           # Pydantic schemas for request/response validation
├── database.py          # SQLite engine and session setup
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker container configuration
├── .dockerignore        # Docker ignore file
├── cookedbook.db        # SQLite database file (auto-generated)
└── templates/           # HTML templates
    ├── index.html       # Home page - list all recipes
    ├── create.html      # Form to create a new recipe
    ├── view.html        # View single recipe details
    └── edit.html        # Form to edit an existing recipe
```

## 📋 Recipe Model

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Auto-generated unique identifier |
| `title` | String | Recipe name |
| `ingredients` | List[Ingredient] | List of ingredients with quantity, unit, name, and notes (stored as JSON) |
| `instructions` | List[String] | Step-by-step cooking instructions |
| `cooking_time` | Integer | Cooking time in minutes |
| `servings` | Integer | Number of servings |
| `category` | Enum | Breakfast, Lunch, Dinner, Dessert, or Snack |

### Ingredient Structure

Each ingredient is stored as a structured object:

| Field | Type | Description |
|-------|------|-------------|
| `quantity` | Float | Numeric quantity (e.g., 2.5) |
| `unit` | String | Unit of measurement (e.g., cups, tbsp, g) |
| `name` | String | Ingredient name (e.g., flour, eggs) |
| `notes` | String | Optional notes (e.g., sifted, room temperature) |

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Home page (HTML) |
| `GET` | `/create` | Create recipe page |
| `GET` | `/recipes/{id}` | View recipe page |
| `GET` | `/recipes/{id}/edit` | Edit recipe page |
| `POST` | `/api/recipes` | Create recipe (JSON API) |
| `GET` | `/api/recipes` | List all recipes (JSON API) |
| `GET` | `/api/recipes/{id}` | Get single recipe (JSON API) |
| `PUT` | `/api/recipes/{id}` | Update recipe (JSON API) |
| `DELETE` | `/api/recipes/{id}` | Delete recipe (JSON API) |

## 🚀 Getting Started

### Prerequisites

- **For Python:** Python 3.13, Conda (recommended) or pip
- **For Docker:** Docker installed on your machine

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/CookedBook.git
   cd CookedBook
   ```

### Running the App

You can run the app using either Python or Docker. Choose the option that works best for you.

#### Option 1: Using Python

1. **Create and activate virtual environment**
   ```bash
   conda create -n CookedBook python=3.13
   conda activate CookedBook
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   python3 -m main
   ```

#### Option 2: Using Docker

1. **Build the Docker image**
   ```bash
   docker build -t cookedbook .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 cookedbook
   ```

---

Then open your browser and navigate to: **http://localhost:8000**

## 🌟 Features

- ✅ Create, read, update, and delete recipes
- ✅ Structured ingredients (quantity, unit, name, notes)
- ✅ Recipe scaling - adjust servings and ingredients scale automatically
- ✅ Categorize recipes (Breakfast, Lunch, Dinner, Dessert, Snack)
- ✅ Track cooking time and servings
- ✅ Beautiful dark mode interface
- ✅ RESTful API for programmatic access
- ✅ Legacy ingredient format migration (automatic parsing of old text-based ingredients)

## 🔮 Future Development Ideas

- 📷 Add recipe photos/images
- 🔍 Add search and filtering functionality
- 📄 Add export to PDF
- 📅 Add meal planning features
- 🖨️ Add print-friendly view
- 👤 Add user authentication
- ⭐ Add recipe ratings and favorites

## 📝 Changelog

### v1.1.0 (Current)
- **Structured Ingredients**: Ingredients now support quantity, unit, name, and notes fields
- **Recipe Scaling**: Scale recipes to any serving size with automatic ingredient adjustment
- **Improved UI**: Add/remove rows for ingredients and instructions with move up/down controls
- **API Enhancement**: Added `original_servings` field to API responses
- **Legacy Support**: Automatic migration of old text-based ingredients to structured format

### v1.0.0
- Initial release
- Basic CRUD operations for recipes
- Recipe categorization (Breakfast, Lunch, Dinner, Dessert, Snack)
- Cooking time and servings tracking
- RESTful API
- Dark mode UI

## 📄 License

This project is licensed under the terms included in the [LICENSE](LICENSE) file.

---

*Made with ❤️ for home cooks everywhere*