from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.exceptions import NotFoundException
from src.users.dependencies import get_current_user
from src.users.models import User

from src.collections.schemas import SCollection, SCollectionCreate
from src.collections.services import CollectionService


router = APIRouter(prefix="/collections", tags=["Collections"])


@router.get("/")
async def get_collections(
    user: Annotated[User, Depends(get_current_user)],
) -> list[SCollection]:
    return await CollectionService.get_all(user=user)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_collection(
    body: SCollectionCreate, user: Annotated[User, Depends(get_current_user)]
):
    await CollectionService.add(name=body.name, user_id=user.id)


@router.get("/{collection_id}")
async def get_one_collection(
    collection_id: int, user: Annotated[User, Depends(get_current_user)]
) -> SCollection:
    collection = await CollectionService.get_one_by_fields(
        id=collection_id, user_id=user.id
    )

    if collection is None:
        raise NotFoundException

    return collection


@router.put("/{collection_id}")
async def update_collection(
    collection_id: int, user: Annotated[User, Depends(get_current_user)]
):
    pass
