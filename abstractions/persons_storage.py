from abc import ABC, abstractmethod
from uuid import UUID
from numpy import ndarray
from typing import List, Union, Tuple
from .user import User

class PersonsStorage(ABC):
    
    @abstractmethod
    async def save(self, person_id: UUID, idx: UUID, feature: ndarray, img: bytes, image_type: str) -> None:
        ...

    @abstractmethod
    async def paged_users(self) -> List[User]:
        ...

    @abstractmethod
    async def neareset(self, feature: []) -> Union[Tuple[User, float], None]:
        ...

    @abstractmethod
    async def get_grants(self, person_id: UUID) -> []:
        ...

