from sqlalchemy import update, and_, delete
from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession

from src.collections.models import Collection
from src.collections.schemas import SCollectionUpdate
from src.services import BaseService


class CollectionService(BaseService):
    model = Collection

    @classmethod
    async def add(cls, session: AsyncSession, **data):
        slug = slugify(data.get("name"))
        await super().add(session=session, slug=slug, **data)

    @classmethod
    async def update_collection(
        cls,
        session: AsyncSession,
        collection_id: int,
        body_data: SCollectionUpdate,
        user_id: int,
    ):
        collection_data = body_data.model_dump(exclude_unset=True)

        stmt = (
            update(cls.model)
            .filter(
                and_(
                    cls.model.id == collection_id,
                    cls.model.user_id == user_id,
                )
            )
            .values(slug=slugify(collection_data.get("name")), **collection_data)
            .returning(cls.model)
        )

        result = await session.execute(stmt)
        await session.commit()

        return result.scalar_one_or_none()

    @classmethod
    async def delete_collection(
        cls,
        session: AsyncSession,
        collection_id: int,
        user_id: int,
    ):
        stmt = (
            delete(cls.model)
            .filter(and_(cls.model.id == collection_id, cls.model.user_id == user_id))
            .returning(cls.model)
        )

        deleted_collection = await session.execute(stmt)
        await session.commit()

        return deleted_collection.scalar_one_or_none()
