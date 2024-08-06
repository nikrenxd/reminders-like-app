from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Model


class User(Model):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]

    collections: Mapped[list["Collection"]] = relationship(back_populates="user")
    tasks: Mapped[list["Task"]] = relationship(back_populates="user")
