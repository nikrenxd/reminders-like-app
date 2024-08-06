import datetime

from pydantic import BaseModel, Field, field_validator
from src.tasks.models import Priority


class STaskCreate(BaseModel):
    name: str = Field(max_length=128)
    description: str | None = Field(default=None, max_length=256)
    priority: Priority
    do_until: datetime.date | None = Field(default=None)
    is_important: bool = False

    @field_validator("name", "priority")
    @classmethod
    def check_if_none_passed(cls, v: str):
        if v is None:
            raise ValueError("None not allowed")

        return v

    @field_validator("do_until")
    @classmethod
    def is_date_valid(cls, v: datetime.date | None):
        if v is None:
            return v

        if not v >= datetime.date.today():
            raise ValueError("Can't pass past date")

        return v


class STask(BaseModel):
    id: int
    name: str
    priority: str
    is_important: bool
    do_until: datetime.date | None
    created_at: datetime.datetime
    updated_at: datetime.datetime


class STaskSingle(STask):
    description: str | None


class STaskUpdate(STaskCreate):
    name: str | None = None
    priority: Priority | None = None


class STaskDone(BaseModel):
    is_done: bool
