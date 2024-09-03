from sqlalchemy import and_, select, update, delete, ScalarSelect

from src.services import BaseService
from src.database import Session

from src.users.models import User
from src.tasks.models import Task
from src.collections.models import Collection
from src.tasks.schemas import STaskSingle, STaskCreate, STaskUpdate, STaskDone


def get_query_filters(**query_filters: dict) -> dict:
    return {param: value for param, value in query_filters.items() if value is not None}


def get_collection_id_stmt(slug: str, user_id: int) -> ScalarSelect:
    return select(Collection.id).filter_by(user_id=user_id, slug=slug).scalar_subquery()


class TaskService(BaseService):
    model = Task

    @classmethod
    async def get_all(cls, collection_slug, user_id, **filters):
        query_filters = get_query_filters(**filters)

        get_tasks = (
            select(cls.model)
            .join(Collection, cls.model.collection_id == Collection.id, isouter=True)
            .filter(
                and_(
                    Collection.slug == collection_slug,
                    cls.model.user_id == user_id,
                )
            )
            .cte("get_tasks")
        )

        stmt = select(get_tasks).filter_by(**query_filters)

        async with Session() as session:
            res = await session.execute(stmt)
            return res.mappings().all()

    @classmethod
    async def get_one_by_fields(cls, collection_slug: str, task_id: int, user_id: int):
        stmt = (
            select(cls.model)
            .join(Collection, cls.model.collection_id == Collection.id)
            .filter(
                and_(
                    Collection.slug == collection_slug,
                    cls.model.id == task_id,
                    cls.model.user_id == user_id,
                )
            )
        )

        async with Session() as session:
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    @classmethod
    async def search_tasks_by_name(cls, user: User, task_name: str):
        stmt = select(cls.model).filter(
            and_(
                cls.model.name.ilike(f"%{task_name}%"),
                cls.model.user == user,
            )
        )
        async with Session() as session:
            res = await session.execute(stmt)
            return res.scalars().all()

    @classmethod
    async def add_task(
        cls,
        collection_slug: str,
        user_id: int,
        task: STaskCreate,
    ) -> int | None:
        task_data = task.model_dump(exclude_unset=True)

        collection_id = get_collection_id_stmt(collection_slug, user_id)
        task_id = await super().add(
            collection_id=collection_id,
            user_id=user_id,
            **task_data,
        )

        return task_id

    @classmethod
    async def update_task(
        cls,
        collection_slug: str,
        task_id: int,
        user_id: int,
        task: STaskUpdate | STaskDone,
    ) -> STaskSingle:
        task_data = task.model_dump(exclude_unset=True)

        collection_id = get_collection_id_stmt(collection_slug)

        update_task = (
            update(cls.model)
            .filter_by(
                collection_id=collection_id,
                id=task_id,
                user_id=user_id,
            )
            .values(**task_data)
            .returning(cls.model)
        )

        async with Session() as session:
            updated_task = await session.execute(update_task)
            await session.commit()

            return updated_task.scalar_one_or_none()

    @classmethod
    async def delete_task(cls, collection_slug: str, task_id: int, user_id: int) -> int:
        collection_id = get_collection_id_stmt(collection_slug)

        delete_task_stmt = (
            delete(cls.model)
            .filter_by(
                collection_id=collection_id,
                id=task_id,
                user_id=user_id,
            )
            .returning(cls.model.id)
        )

        async with Session() as session:
            task_id = await session.execute(delete_task_stmt)
            await session.commit()

        return task_id.scalar()
