from sqlalchemy import insert, select

from src.database import Session


class BaseService:
    model = None

    @classmethod
    async def get_all(cls, **filters):
        async with Session() as session:
            stmt = select(cls.model).filter_by(**filters)
            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def get_one_by_fields(cls, **fields):
        async with Session() as session:
            stmt = select(cls.model).filter_by(**fields)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **data):
        async with Session() as session:
            stmt = insert(cls.model).values(**data)
            await session.execute(stmt)
            await session.commit()
