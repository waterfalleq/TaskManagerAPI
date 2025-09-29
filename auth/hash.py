from passlib.context import CryptContext

ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(plain_password: str) -> str:
    """Hash plain text password with bcrypt."""
    return ctx.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if plain password matches the hash."""
    return ctx.verify(plain_password, hashed_password)
