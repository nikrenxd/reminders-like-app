import enum
from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from src.database import Model
from src.users.models import User
from src.collections.models import Collection
from src.tags.models import Tag


class Priority(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Task(Model):
    __tablename__ = "tasks"

    name: Mapped[str] = mapped_column(String(128), index=True)
    description: Mapped[str | None] = mapped_column(String(256))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    collection_id: Mapped[int] = mapped_column(
        ForeignKey("collections.id", ondelete="CASCADE"), index=True
    )

    is_important: Mapped[bool] = mapped_column(default=False, index=True)
    is_done: Mapped[bool] = mapped_column(default=False)
    priority: Mapped[Priority]
    do_until: Mapped[date | None]

    user: Mapped["User"] = relationship(back_populates="tasks")
    collection: Mapped["Collection"] = relationship(back_populates="tasks")
    tags_include: Mapped[list["Tag"]] = relationship(
        back_populates="tasks_include",
        secondary="tags_tasks",
    )
