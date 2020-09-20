import uuid
from abc import ABC, abstractmethod


class ImagesStorage(ABC):

    @abstractmethod
    async def save(self, person_id: uuid.UUID, image_type: str, feature_id: uuid.UUID, image: bytes) -> None:
        ...

    @abstractmethod
    async def delete(self, person_id: uuid.UUID, feature_id: uuid.UUID) -> None:
        ...

    @abstractmethod
    async def get(self, person_id: uuid.UUID, feature_id: uuid.UUID):
        ...

    @abstractmethod
    async def delete_for_user(self, person_id: uuid.UUID) -> None:
        ...