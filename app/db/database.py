from os import getenv

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

ENV = getenv("ENV", "local")
if ENV == "docker":
    DATABASE_URL = getenv("DATABASE_URL_DOCKER")
else:
    DATABASE_URL = getenv("DATABASE_URL_LOCAL")

async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Yield a database session and ensure it closes after use."""
    async with async_session() as session:
        yield session
