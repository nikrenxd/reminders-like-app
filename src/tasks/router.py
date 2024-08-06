from fastapi import APIRouter, Depends, status, Query
from typing import Annotated

from src.users.models import User
from src.users.dependencies import get_current_user

from src.tasks.services import TaskService
from src.tasks.schemas import STask, STaskCreate, STaskSingle, STaskDone
from src.tasks.dependencies import RoutesIdParams, RoutesUpdateParams, RoutesFindParams

from src.exceptions import NotFoundException

router = APIRouter(prefix="/{collection_name}/tasks", tags=["Tasks"])


@router.get("/")
async def get_all_tasks(params: Annotated[RoutesFindParams, Depends()]) -> list[STask]:
    query_params = {}

    if params.only_with_priority:
        query_params.update({"priority": params.only_with_priority})
    if params.show_important:
        query_params.update({"is_important": params.show_important})
    if params.show_done:
        query_params.update({"is_done": params.show_done})

    return await TaskService.get_all(user=params.user, **query_params)


@router.get("/search")
async def search_task(
    search_by_name: Annotated[str, Query()],
    params: Annotated[RoutesFindParams, Depends()],
) -> list[STask]:
    return await TaskService.search_tasks_by_name(
        user=params.user,
        task_name=search_by_name,
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(
    body: STaskCreate, user: Annotated[User, Depends(get_current_user)]
) -> None:
    await TaskService.add(
        name=body.name,
        description=body.description,
        priority=body.priority,
        do_until=body.do_until,
        user_id=user.id,
    )


@router.get("/{task_id}")
async def get_task(params: Annotated[RoutesIdParams, Depends()]) -> STaskSingle:
    task = await TaskService.get_one_by_fields(id=params.task_id, user=params.user)

    if not task:
        raise NotFoundException

    return task


@router.put("/{task_id}")
async def update_task(params: Annotated[RoutesUpdateParams, Depends()]) -> STaskSingle:
    task = await TaskService.update_task(params.task_id, params.user.id, params.body)

    if not task:
        raise NotFoundException

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(params: Annotated[RoutesIdParams, Depends()]):
    task = await TaskService.delete_task(params.task_id, params.user.id)

    if not task:
        raise NotFoundException


@router.patch("/{task_id}/done")
async def done_task(body: STaskDone, params: Annotated[RoutesIdParams, Depends()]):
    await TaskService.update_task(params.task_id, params.user.id, body)
