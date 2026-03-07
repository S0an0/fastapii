from passlib.context import CryptContext
from src.core.config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=settings.BCRYPT_ROUNDS
)

async def hash_password(password: str) -> str:
    return pwd_context.hash(password)