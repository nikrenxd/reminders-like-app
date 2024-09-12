from pydantic import BaseModel, Field
from src.collections.models import CollectionColor


class SCollectionCreate(BaseModel):
    name: str = Field(max_length=128)
    color: CollectionColor = Field(default=CollectionColor.blue.value)


class SCollection(SCollectionCreate):
    id: int


class SCollectionUpdate(SCollectionCreate):
    pass
