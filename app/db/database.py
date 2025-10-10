from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

ENV = getenv("ENV", "local")
if ENV == "docker":
    DATABASE_URL = getenv("DATABASE_URL_DOCKER")
else:
    DATABASE_URL = getenv("DATABASE_URL_LOCAL")

engine = create_engine(
    DATABASE_URL, echo=True  # Log SQL queries, set False in production
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Yield a database session and ensure it closes after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
