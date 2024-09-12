from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.users.services import UserService
from src.users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def create_jwt_token(data: dict) -> str:
    to_encode = data.copy()
    expiration_time = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expiration_time})
    token = jwt.encode(to_encode, settings.JWT_SECRET, settings.JWT_ALGORITHM)
    return token


async def authenticate_user(
    session: AsyncSession,
    email: str,
    password: str,
) -> User | None:
    existing_user = await UserService.get_one_by_fields(session, email=email)

    if not existing_user:
        return None

    password_correct = verify_password(password, existing_user.password)

    if not password_correct:
        return None

    return existing_user
