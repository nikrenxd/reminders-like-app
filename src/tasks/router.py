from fastapi import APIRouter, Depends, status, Query
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.users.models import User
from src.users.dependencies import get_current_user

from src.tasks.services import TaskService
from src.tasks.schemas import STask, STaskCreate, STaskSingle, STaskDone
from src.tasks.dependencies import ParamsWithId, UpdateParams, FindParams

from src.exceptions import NotFoundException

router = APIRouter(prefix="/{collection_slug}/tasks", tags=["Tasks"])


@router.get("/")
async def get_all_tasks(
    session: Annotated[AsyncSession, Depends(get_session)],
    params: Annotated[FindParams, Depends()],
) -> list[STask]:
    tasks = await TaskService.get_all(
        session,
        collection_slug=params.collection_slug,
        user_id=params.user.id,
        is_done=params.done,
        priority=params.priority,
        is_important=params.important,
    )

    if not tasks:
        raise NotFoundException

    return tasks


# TODO: Update search endpoint
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(
    collection_slug: str,
    body: STaskCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
) -> int | None:
    task_id = await TaskService.add_task(
        session,
        collection_slug=collection_slug,
        user_id=user.id,
        task=body,
    )

    return task_id


@router.get("/search", include_in_schema=False)
async def search_task(
    search_by_name: Annotated[str, Query()],
    params: Annotated[FindParams, Depends()],
) -> list[STask]:
    return await TaskService.search_tasks_by_name(
        user=params.user,
        task_name=search_by_name,
    )


@router.get("/{task_id}")
async def get_task(
    session: Annotated[AsyncSession, Depends(get_session)],
    params: Annotated[ParamsWithId, Depends()],
) -> STaskSingle:
    task = await TaskService.get_one_by_fields(
        session,
        collection_slug=params.collection_slug,
        task_id=params.task_id,
        user_id=params.user.id,
    )

    if not task:
        raise NotFoundException

    return task


@router.put("/{task_id}")
async def update_task(
    session: Annotated[AsyncSession, Depends(get_session)],
    params: Annotated[UpdateParams, Depends()],
) -> STaskSingle:
    task = await TaskService.update_task(
        session,
        params.collection_slug,
        params.task_id,
        params.user.id,
        params.body,
    )

    if not task:
        raise NotFoundException

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    session: Annotated[AsyncSession, Depends(get_session)],
    params: Annotated[ParamsWithId, Depends()],
):
    task = await TaskService.delete_task(
        session,
        params.collection_slug,
        params.task_id,
        params.user.id,
    )

    if not task:
        raise NotFoundException


@router.patch("/{task_id}/done")
async def done_task(
    params: Annotated[ParamsWithId, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
    done_param: Annotated[bool, Query()] = True,
) -> STaskSingle:
    task_done = STaskDone(is_done=done_param)

    task = await TaskService.update_task(
        session,
        params.collection_slug,
        params.task_id,
        params.user.id,
        task_done,
    )

    if not task:
        raise NotFoundException

    return task
