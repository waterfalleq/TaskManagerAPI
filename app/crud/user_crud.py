from pydantic import EmailStr
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User
from app.auth.hash import get_password_hash, verify_password


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Fetch a user by email."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, id: int) -> User | None:
    """Fetch a user by ID."""
    result = await db.execute(select(User).where(User.id == id))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, email: str, plain_password: str) -> User:
    """Create a new user with a hashed password."""
    existing_user = await get_user_by_email(db, email)
    if existing_user is not None:
        raise HTTPException(
            status_code=409, detail="Account with this email already exists"
        )
    new_user = User(email=email, hashed_password=get_password_hash(plain_password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_user_email(db: AsyncSession, user: User, new_email: EmailStr) -> User:
    """Update an existing user's email address."""
    existing_user = await get_user_by_email(db, new_email)
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.email = new_email
    await db.commit()
    await db.refresh(user)
    return user


async def update_user_password(
    db: AsyncSession, user: User, old_password: str, new_password: str
) -> User:
    """Update an existing user's password."""
    if not verify_password(old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    user.hashed_password = get_password_hash(new_password)
    await db.commit()
    await db.refresh(user)
    return user
