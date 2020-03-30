from abc import ABC
from typing import List
from uuid import UUID


class GrantsCrypto(ABC):
    def to_token(self, person_id: UUID, grants : List[str]) -> str:
        pass