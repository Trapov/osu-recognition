from abc import ABC, abstractmethod
from typing import List, Tuple
from uuid import UUID


class GrantsCrypto(ABC):
    @abstractmethod
    def to_token(self, person_id: UUID, grants : List[str]) -> str:
        pass

    @abstractmethod
    def to_user_id_with_grants(self, token: str) -> Tuple[UUID, List[str]]:
        ...