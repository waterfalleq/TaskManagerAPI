from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt_handler import get_current_user
from app.crud.user_crud import update_user_email, update_user_password
from app.db.database import get_db
from app.models.models import User
from app.schemas.user import UserResponse, UpdateEmailRequest, UpdatePasswordRequest

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user's information."""
    return current_user


@router.patch("/email", response_model=UserResponse)
async def update_email(
    request: UpdateEmailRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update the current user's email address."""
    updated_user = await update_user_email(
        db=db, user=current_user, new_email=request.email
    )
    return updated_user


@router.patch("/password")
async def update_password(
    request: UpdatePasswordRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update the current user's password."""
    await update_user_password(
        db=db,
        user=current_user,
        old_password=request.old_password,
        new_password=request.new_password,
    )
    return {"detail": "Password updated successfully"}
