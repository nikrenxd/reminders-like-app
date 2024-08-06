from src.services.base import BaseService
from src.collections.models import Collection


class CollectionService(BaseService):
    model = Collection
