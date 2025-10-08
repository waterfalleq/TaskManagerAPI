from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from datetime import datetime
import re


def validate_password_complexity(password: str) -> str:
    """
    Validates the complexity of a password.
    Requirements:
    1. At least 8 characters long.
    2. Contains at least one uppercase letter (A-Z).
    3. Contains at least one lowercase letter (a-z).
    4. Contains at least one digit (0-9).
    5. Contains at least one special character (e.g., !@#$%^&*(),.?":{}|<>).
    """
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one digit")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("Password must contain at least one special character")
    return password


class UserBase(BaseModel):
    """Base fields shared by all user models."""

    email: EmailStr


class UserCreate(UserBase):
    """Fields required to register a new user."""

    password: str

    @field_validator("password")
    def password_complexity(cls, v):
        return validate_password_complexity(v)


class UserLogin(UserBase):
    """Fields required for user login."""

    password: str


class UserResponse(UserBase):
    """Response model for user info with ID and creation timestamp."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """JWT token response model."""

    access_token: str
    token_type: str


class UpdateEmailRequest(BaseModel):
    email: EmailStr


class UpdatePasswordRequest(BaseModel):
    old_password: str
    new_password: str

    @field_validator("new_password")
    def password_complexity(cls, v):
        return validate_password_complexity(v)
