from fastapi import APIRouter, Depends

from auth.jwt_handler import get_current_user
from models.models import User
from schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user's information."""
    return current_user
