from src.services.base import BaseService

from src.users.models import User


class UserService(BaseService):
    model = User
