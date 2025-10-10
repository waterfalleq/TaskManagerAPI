from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.hash import verify_password
from app.auth.jwt_handler import create_access_token
from app.crud.user_crud import get_user_by_email, create_user
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(
    user: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """Register a new user with email and password."""
    new_user = await create_user(db, email=user.email, plain_password=user.password)
    return new_user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
) -> Token:
    """Authenticate user and return a JWT access token."""
    user = await get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = {"sub": str(user.id)}
    access_token = create_access_token(data=payload)
    return {"access_token": access_token, "token_type": "bearer"}
