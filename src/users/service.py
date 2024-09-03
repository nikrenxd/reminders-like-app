from src.services import BaseService

from src.users.models import User


class UserService(BaseService):
    model = User
