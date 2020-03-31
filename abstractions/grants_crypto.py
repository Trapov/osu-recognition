from abc import ABC, abstractmethod
from typing import List
from uuid import UUID


class GrantsCrypto(ABC):
    @abstractmethod
    def to_token(self, person_id: UUID, grants : List[str]) -> str:
        pass