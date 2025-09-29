from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    """Base fields shared by all user models."""

    email: EmailStr


class UserCreate(UserBase):
    """Fields required to register a new user."""

    password: str = Field(min_length=8)


class UserLogin(UserBase):
    """Fields required for user login."""

    password: str = Field(min_length=8)


class UserResponse(UserBase):
    """Response model for user info with ID and creation timestamp."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """JWT token response model."""

    access_token: str
    token_type: str
