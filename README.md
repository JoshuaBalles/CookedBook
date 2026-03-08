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
| `ingredients` | List[String] | List of ingredients (stored as JSON) |
| `instructions` | List[String] | Step-by-step cooking instructions |
| `cooking_time` | Integer | Cooking time in minutes |
| `servings` | Integer | Number of servings |
| `category` | Enum | Breakfast, Lunch, Dinner, Dessert, or Snack |

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

- Python 3.9 or higher
- Conda (recommended) or pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/CookedBook.git
   cd CookedBook
   ```

2. **Create and activate virtual environment**
   ```bash
   conda create -n CookedBook python=3.11
   conda activate CookedBook
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

```bash
python3 -m main
```

Then open your browser and navigate to: **http://localhost:8000**

## 🌟 Features

- ✅ Create, read, update, and delete recipes
- ✅ Categorize recipes (Breakfast, Lunch, Dinner, Dessert, Snack)
- ✅ Track cooking time and servings
- ✅ Beautiful dark mode interface
- ✅ RESTful API for programmatic access

## 🔮 Future Development Ideas

- 📷 Add recipe photos/images
- 🔍 Add search and filtering functionality
- 📐 Add ingredient scaling
- 📄 Add export to PDF
- 📅 Add meal planning features
- 🖨️ Add print-friendly view
- 👤 Add user authentication
- ⭐ Add recipe ratings and favorites

## 📄 License

This project is licensed under the terms included in the [LICENSE](LICENSE) file.

---

*Made with ❤️ for home cooks everywhere*