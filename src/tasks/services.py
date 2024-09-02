from sqlalchemy import and_, select, insert, update, delete, ScalarSelect

from src.services.base import BaseService
from src.database import Session

from src.users.models import User
from src.tasks.models import Task
from src.collections.models import Collection
from src.tasks.schemas import STaskSingle, STaskCreate


def get_query_filters(**query_filters: dict) -> dict:
    return {param: value for param, value in query_filters.items() if value is not None}


def get_collection_id_stmt(slug: str) -> ScalarSelect:
    return select(Collection.id).filter_by(slug=slug).scalar_subquery()


class TaskService(BaseService):
    model = Task

    @classmethod
    async def get_all(cls, collection_name, user_id, **filters):
        query_filters = get_query_filters(**filters)

        get_tasks = (
            select(cls.model)
            .join(Collection, cls.model.collection_id == Collection.id)
            .filter(
                and_(
                    Collection.slug == collection_name,
                    cls.model.user_id == user_id,
                )
            )
        ).cte("get_tasks")

        stmt = select(
            get_tasks.c.id,
            get_tasks.c.name,
            get_tasks.c.priority,
            get_tasks.c.priority,
            get_tasks.c.is_important,
            get_tasks.c.do_until,
            get_tasks.c.created_at,
            get_tasks.c.updated_at,
        ).filter_by(**query_filters)

        async with Session() as session:
            res = await session.execute(stmt)
            return res.mappings().all()

    @classmethod
    async def get_one_by_fields(cls, collection_name: str, task_id: int, user_id: int):
        stmt = (
            select(cls.model)
            .join(Collection, cls.model.collection_id == Collection.id)
            .filter(
                and_(
                    Collection.slug == collection_name,
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
    async def add(cls, collection_name: str, user_id: int, task: STaskCreate) -> int:
        task_data = task.model_dump(exclude_unset=True)

        collection_id = get_collection_id_stmt(collection_name)

        insert_task = (
            insert(cls.model)
            .values(collection_id=collection_id, user_id=user_id, **task_data)
            .returning(cls.model.id)
        )

        async with Session() as session:
            task_id = await session.execute(insert_task)
            await session.commit()

        return task_id.scalar()

    @classmethod
    async def update_task(
        cls, collection_name: str, task_id: int, user_id: int, task
    ) -> STaskSingle:
        task_data = task.model_dump(exclude_unset=True)

        collection_id = get_collection_id_stmt(collection_name)

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
    async def delete_task(cls, collection_name: str, task_id: int, user_id: int) -> int:
        collection_id = get_collection_id_stmt(collection_name)

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
