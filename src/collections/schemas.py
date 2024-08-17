from pydantic import BaseModel, Field


class SCollectionCreate(BaseModel):
    name: str = Field(max_length=128)


class SCollection(SCollectionCreate):
    id: int


class SCollectionUpdate(SCollectionCreate):
    pass
