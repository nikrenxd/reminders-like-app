from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import text

from src.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)

Session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow
    )


async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session
