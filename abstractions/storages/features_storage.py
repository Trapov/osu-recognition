import uuid
from abc import ABC, abstractmethod
from typing import List, AsyncIterator
from ..user import UserFeatures, Feature
from datetime import datetime

class FeaturesStorage(ABC):
    @abstractmethod
    async def save(self, person_id: uuid.UUID, feature_id: uuid.UUID, image_type: str, feature: bytes, created_at: datetime, transaction_scope = None) -> None:
        ...

    @abstractmethod
    async def delete(self, user_id: uuid.UUID, idx: uuid.UUID, transaction_scope = None) -> None:
        ...

    @abstractmethod
    async def enumerate_for(self, idx : uuid.UUID) -> AsyncIterator[UserFeatures]:
        ...

    @abstractmethod
    async def enumerate(self) -> AsyncIterator[UserFeatures]:
        ...
