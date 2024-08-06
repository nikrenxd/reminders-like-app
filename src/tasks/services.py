from sqlalchemy import update, and_, delete, select, or_

from src.services.base import BaseService
from src.database import Session

from src.users.models import User
from src.tasks.models import Task
from src.tasks.schemas import STaskUpdate, STaskSingle


class TaskService(BaseService):
    model = Task

    @classmethod
    async def search_tasks_by_name(cls, user: User, task_name: str):
        async with Session() as session:
            stmt = (
                select(cls.model)
                .filter(
                    and_(
                        cls.model.name.ilike(f"%{task_name}%"),
                        cls.model.user == user,
                    )
                )
            )

            res = await session.execute(stmt)
            return res.scalars().all()

    @classmethod
    async def update_task(cls, task_id: int, user_id: int, task) -> STaskSingle:
        task_data = task.model_dump(exclude_unset=True)

        async with Session() as session:
            update_task = (
                update(cls.model)
                .filter(and_(cls.model.id == task_id, cls.model.user_id == user_id))
                .values(**task_data)
                .returning(cls.model)
            )

            result = await session.execute(update_task)
            await session.commit()

            return result.scalar_one_or_none()

    @classmethod
    async def delete_task(cls, task_id, user_id):
        async with Session() as session:
            stmt = (
                delete(cls.model)
                .filter(and_(cls.model.id == task_id, cls.model.user_id == user_id))
                .returning(cls.model)
            )

            deleted_task = await session.execute(stmt)
            await session.commit()

            return deleted_task.scalar_one_or_none()
