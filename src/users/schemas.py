from pydantic import BaseModel, EmailStr, Field


class SUserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4, max_length=12)


class SUserLogin(SUserCreate):
    password: str
