import uuid
from abc import ABC, abstractmethod
from typing import List, AsyncIterator
from ..user import UserFeatures, Feature
from datetime import datetime

class FeaturesStorage(ABC):
    @abstractmethod
    async def save(self, person_id: uuid.UUID, feature_id: uuid.UUID, image_type: str, feature: bytes, created_at: datetime) -> None:
        ...

    @abstractmethod
    async def enumerate(self) -> AsyncIterator[UserFeatures]:
        ...
