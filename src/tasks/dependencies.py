from typing import Annotated
from fastapi import Depends, Query

from src.users.models import User
from src.users.dependencies import get_current_user

from src.tasks.schemas import STaskUpdate
from src.tasks.models import Priority


class RoutesIdParams:
    def __init__(self, task_id: int, user: Annotated[User, Depends(get_current_user)]):
        self.task_id = task_id
        self.user = user


class RoutesFindParams:
    def __init__(
        self,
        user: Annotated[User, Depends(get_current_user)],
        show_done: Annotated[bool, Query()] = False,
        only_with_priority: Annotated[Priority, Query()] = None,
        show_important: Annotated[bool, Query()] = None,
    ):
        self.user = user
        self.show_done = show_done
        self.only_with_priority = only_with_priority
        self.show_important = show_important


class RoutesUpdateParams(RoutesIdParams):
    def __init__(
        self,
        body: STaskUpdate,
        task_id: int,
        user: Annotated[User, Depends(get_current_user)],
    ):
        self.body = body
        super().__init__(task_id, user)
