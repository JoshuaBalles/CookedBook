from sqlmodel import SQLModel, create_engine, Session

# SQLite database URL
DATABASE_URL = "sqlite:///cookedbook.db"

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """Create all database tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get a database session."""
    with Session(engine) as session:
        yield session
