from fastapi import APIRouter, Depends, status, Query
from typing import Annotated

from src.users.models import User
from src.users.dependencies import get_current_user

from src.tasks.services import TaskService
from src.tasks.schemas import STask, STaskCreate, STaskSingle, STaskDone
from src.tasks.dependencies import ParamsWithId, UpdateParams, FindParams

from src.exceptions import NotFoundException

router = APIRouter(prefix="/{collection_name}/tasks", tags=["Tasks"])


@router.get("/")
async def get_all_tasks(params: Annotated[FindParams, Depends()]) -> list[STask]:
    return await TaskService.get_all(
        collection_name=params.collection_name,
        user_id=params.user.id,
        is_done=params.done,
        priority=params.priority,
        is_important=params.important,
    )


@router.get("/search")
async def search_task(
    search_by_name: Annotated[str, Query()],
    params: Annotated[FindParams, Depends()],
) -> list[STask]:
    return await TaskService.search_tasks_by_name(
        user=params.user,
        task_name=search_by_name,
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(
    collection_name: str,
    body: STaskCreate,
    user: Annotated[User, Depends(get_current_user)],
) -> int:
    return await TaskService.add(
        collection_name=collection_name, user_id=user.id, task=body
    )


@router.get("/{task_id}")
async def get_task(params: Annotated[ParamsWithId, Depends()]) -> STaskSingle:
    task = await TaskService.get_one_by_fields(
        collection_name=params.collection_name,
        task_id=params.task_id,
        user_id=params.user.id,
    )

    if not task:
        raise NotFoundException

    return task


@router.put("/{task_id}")
async def update_task(params: Annotated[UpdateParams, Depends()]) -> STaskSingle:
    task = await TaskService.update_task(
        params.collection_name, params.task_id, params.user.id, params.body
    )

    if not task:
        raise NotFoundException

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(params: Annotated[ParamsWithId, Depends()]):
    task = await TaskService.delete_task(
        params.collection_name, params.task_id, params.user.id
    )

    if not task:
        raise NotFoundException


@router.patch("/{task_id}/done")
async def done_task(body: STaskDone, params: Annotated[ParamsWithId, Depends()]):
    await TaskService.update_task(params.task_id, params.user.id, body)
