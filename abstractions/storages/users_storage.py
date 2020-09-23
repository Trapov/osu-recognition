import uuid, datetime
from abc import ABC, abstractmethod
from typing import AsyncIterator

from abstractions import User


class UsersStorage(ABC):

    @abstractmethod
    async def single_no_features(self, user_id: uuid.UUID):
        ...

    @abstractmethod
    async def upsert(self, user_id: uuid.UUID, created_at: datetime.datetime, transaction_scope = None) -> None:
        ...
        
    @abstractmethod
    async def save(self, user: User, transaction_scope = None) -> None:
        ...

    @abstractmethod
    async def enumerate(self, offset: int = None, limit: int = None) -> AsyncIterator[User]:
        ...

    @abstractmethod
    async def delete_grant(self, user_id: uuid.UUID, grant: str, transaction_scope = None) -> None:
        ...

    @abstractmethod
    async def delete_user(self, user_id: uuid.UUID, transaction_scope = None) -> None:
        ...

    @abstractmethod
    async def count(self) -> int:
        ...
