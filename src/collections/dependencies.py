from typing import Annotated
from fastapi import Depends

from src.users.models import User
from src.users.dependencies import get_current_user
from src.collections.schemas import SCollectionUpdate


class ParamsWithId:
    def __init__(
        self, collection_id: int, user: Annotated[User, Depends(get_current_user)]
    ):
        self.collection_id = collection_id
        self.user = user


class UpdateParams(ParamsWithId):
    def __init__(
        self,
        body: SCollectionUpdate,
        collection_id: int,
        user: Annotated[User, Depends(get_current_user)],
    ):
        self.body = body
        super().__init__(collection_id, user)
