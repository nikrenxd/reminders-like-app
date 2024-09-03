from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError

from src.database import Session
from src.exceptions import AddException


class BaseService:
    model = None

    @classmethod
    async def get_all(cls, **filters):
        stmt = select(cls.model).filter_by(**filters)

        async with Session() as session:
            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def get_one_by_fields(cls, **fields):
        stmt = select(cls.model).filter_by(**fields)

        async with Session() as session:
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **data) -> int | None:
        stmt = insert(cls.model).values(**data).returning(cls.model.id)

        try:
            async with Session() as session:
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar_one()
        except SQLAlchemyError:
            raise AddException
