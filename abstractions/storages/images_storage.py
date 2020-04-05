import uuid
from abc import ABC, abstractmethod


class ImagesStorage(ABC):

    @abstractmethod
    async def save(self, person_id: uuid.UUID, image_type: str, feature_id: uuid.UUID, image: bytes) -> None:
        ...
