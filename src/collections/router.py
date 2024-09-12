from typing import Annotated

from fastapi import APIRouter, Depends, status

from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from src.collections.schemas import SCollection, SCollectionCreate
from src.collections.services import CollectionService
from src.database import get_session
from src.exceptions import NotFoundException
from src.users.dependencies import get_current_user
from src.users.models import User
from src.collections.dependencies import UpdateParams, ParamsWithId

router = APIRouter(prefix="/collections", tags=["Collections"])


@router.get("/", response_model=list[SCollection])
@cache(expire=15)
async def get_collections(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await CollectionService.get_all(session, user=user)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_collection(
    body: SCollectionCreate,
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    await CollectionService.add(session, name=body.name, user_id=user.id)


@router.put("/{collection_id}", response_model=SCollection)
async def update_collection(
    session: Annotated[AsyncSession, Depends(get_session)],
    params: Annotated[UpdateParams, Depends()],
):
    collection = await CollectionService.update_collection(
        session,
        params.collection_id,
        params.body,
        params.user.id,
    )

    if not collection:
        raise NotFoundException

    return collection


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(
    session: Annotated[AsyncSession, Depends(get_session)],
    params: Annotated[ParamsWithId, Depends()],
) -> None:
    collection = await CollectionService.delete_collection(
        session,
        params.collection_id,
        params.user.id,
    )

    if not collection:
        raise NotFoundException
