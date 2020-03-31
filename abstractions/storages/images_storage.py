import uuid
from typing import List, Callable, Iterator
from abc import ABC, abstractmethod

class PersonImages():
    def __init__(self, person_id : uuid.UUID, images_names : List[str]):
        self.images_names : List[str] = images_names
        self.person_id : uuid.UUID = person_id

    def __str__(self):
        return f'Person[{str(self.person_id)}] [ {self.images_names} ]'

class ImagesStorage(ABC):

    @abstractmethod
    async def save(self, person_id: uuid.UUID, image_type: str, feature_id: uuid.UUID, image: bytes) -> None:
        ...

    @abstractmethod
    async def enumerate(self, persons_filter: Callable[[str], bool] = lambda f : True) -> Iterator[PersonImages]:
        ...