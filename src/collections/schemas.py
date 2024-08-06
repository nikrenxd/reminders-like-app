from pydantic import BaseModel


class SCollectionCreate(BaseModel):
    name: str


class SCollection(SCollectionCreate):
    id: int
