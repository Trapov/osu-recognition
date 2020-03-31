import uuid
from typing import List, Callable, Iterator
from abc import ABC, abstractmethod


class PersonGrants():
    def __init__(self, person_id : uuid.UUID, grants: List[str]):
        self.grants : List[str] = grants
        self.person_id : uuid.UUID = person_id

    def __str__(self):
        return f'Person[{str(self.person_id)}] [{self.grants}] ]'

class GrantsStorage(ABC):
    @abstractmethod
    async def enumerate(self, persons_filter: Callable[[str], bool] = lambda f : True) -> Iterator[PersonGrants]:
        ...

