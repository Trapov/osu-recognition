from abc import ABC, abstractmethod
from uuid import UUID
from numpy import ndarray
from typing import List, Union
from .user import User

class PersonsStorage(ABC):
    
    @abstractmethod
    def save(self, person_id: UUID, idx: UUID, feature: ndarray) -> None:
        ...

    @abstractmethod
    def paged_users(self) -> List[User]:
        ...

    @abstractmethod
    def neareset(self, feature: []) -> Union[User, None]:
        ...

