from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from src.database import Model


class Tag(Model):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String(32), index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    tasks_include: Mapped[list["Task"]] = relationship(
        back_populates="tags_include",
        secondary="tags_tasks",
    )


class TagTask(Model):
    __tablename__ = "tags_tasks"

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True,
    )
    tags_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    )
