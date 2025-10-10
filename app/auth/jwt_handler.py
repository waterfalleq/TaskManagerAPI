from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from dotenv import load_dotenv
import os

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user_crud import get_user_by_id
from app.db.database import get_db

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generate JWT access token with expiration."""
    payload = data.copy()

    now = datetime.now(timezone.utc)
    payload["iat"] = int(now.timestamp())

    expire = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload["exp"] = int(expire.timestamp())

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Decode and validate JWT access token."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token is expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """Retrieve current authenticated user from token."""
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = await get_user_by_id(db, int(user_id))
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token is expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token is invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )
