from sqlalchemy.orm import Session
from fastapi import HTTPException


from models.models import User
from auth.hash import get_password_hash


def get_user_by_email(db: Session, email: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    return user


def get_user_by_id(db: Session, id: int) -> User | None:
    user = db.query(User).filter(User.id == id).first()
    return user


def create_user(db: Session, email: str, plain_password: str) -> User:
    if get_user_by_email(db, email) is not None:
        raise HTTPException(
            status_code=409, detail="Account with this email already exists"
        )
    new_user = User(email=email, hashed_password=get_password_hash(plain_password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
