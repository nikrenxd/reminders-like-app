from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.collections.schemas import SCollection, SCollectionCreate
from src.collections.services import CollectionService
from src.exceptions import NotFoundException
from src.users.dependencies import get_current_user
from src.users.models import User
from src.collections.dependencies import UpdateParams, ParamsWithId

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


@router.put("/{collection_id}")
async def update_collection(params: Annotated[UpdateParams, Depends()]) -> SCollection:
    collection = await CollectionService.update_collection(
        params.collection_id, params.body, params.user.id
    )

    if not collection:
        raise NotFoundException

    return collection


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(params: Annotated[ParamsWithId, Depends()]) -> None:
    collection = await CollectionService.delete_collection(
        params.collection_id, params.user.id
    )

    if not collection:
        raise NotFoundException
