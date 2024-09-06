from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import AddException


class BaseService:
    model = None

    @classmethod
    async def get_all(cls, session: AsyncSession, **filters):
        stmt = select(cls.model).filter_by(**filters)

        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def get_one_by_fields(cls, session: AsyncSession, **fields):
        stmt = select(cls.model).filter_by(**fields)

        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def add(cls, session: AsyncSession, **data) -> int | None:
        stmt = insert(cls.model).values(**data).returning(cls.model.id)

        try:
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()
        except SQLAlchemyError:
            raise AddException
