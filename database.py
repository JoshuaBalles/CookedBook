from sqlmodel import SQLModel, create_engine, Session
import os

# Database file path - uses DATA_DIR env var (defaults to current directory for local dev)
# In Docker, DATA_DIR is set to /data via docker-compose.yml
DATA_DIR = os.environ.get("DATA_DIR", ".")
DB_FILE = os.path.join(DATA_DIR, "cookedbook.db")

# SQLite database URL
DATABASE_URL = f"sqlite:///{DB_FILE}"

# Create the engine (echo enabled only in debug mode)
engine = create_engine(DATABASE_URL, echo=os.environ.get("DEBUG", "false").lower() == "true")


def create_db_and_tables():
    """Create all database tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get a database session."""
    with Session(engine) as session:
        yield session
