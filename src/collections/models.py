from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from src.database import Model
from src.users.models import User


class Collection(Model):
    __tablename__ = "collections"

    name: Mapped[str] = mapped_column(String(128), index=True, unique=True)
    slug: Mapped[str] = mapped_column(unique=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )

    user: Mapped["User"] = relationship(back_populates="collections")
    tasks: Mapped[list["Task"]] = relationship(back_populates="collection")
