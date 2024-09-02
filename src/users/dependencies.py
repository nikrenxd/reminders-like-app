from typing import Annotated
from datetime import datetime

from fastapi import Request, Depends
from jose import jwt, JWTError

from src.config import settings
from src.exceptions import (
    TokenAbsentException,
    IncorrectTokenFormatException,
    TokenExpiredException,
    UserIsNotPresentException,
)

from src.users.models import User
from src.users.service import UserService


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise TokenAbsentException

    return token


async def get_current_user(token: Annotated[get_token, Depends()]) -> User:
    try:
        data = jwt.decode(token, settings.JWT_SECRET, settings.JWT_ALGORITHM)
    except JWTError:
        raise IncorrectTokenFormatException

    expire: str = data.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException

    user_id: int = data.get("sub")
    if not user_id:
        raise UserIsNotPresentException

    user: User = await UserService.get_one_by_fields(id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user
