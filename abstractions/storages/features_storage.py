import uuid
from typing import List, Tuple, Callable, Iterator
from abc import ABC, abstractmethod

class Feature():
    def __init__(self, feature_id : uuid.UUID, feature: bytes):
        self.feature_id : uuid.UUID = feature_id
        self.feature : bytes = feature

    def __str__(self):
        return f'Feature[{str(self.feature_id)}] [{len(self.feature)}] bytes.'

class PersonFeatures():
    def __init__(self, person_id : uuid.UUID, features: List[Feature]):
        self.features : List[Feature] = features
        self.person_id : uuid.UUID = person_id

    def __str__(self):
        return f'Person[{str(self.person_id)}] [ {[str(feature) for feature in self.features]} ]'

class FeaturesStorage(ABC):
    @abstractmethod
    async def save(self, person_id: uuid.UUID, feature_id: uuid.UUID, feature: bytes) -> None:
        ...

    @abstractmethod
    async def enumerate(self, persons_filter: Callable[[str], bool] = lambda f : True) -> Iterator[PersonFeatures]:
        ...

    @abstractmethod
    async def enumerate_features_idxs(self, persons_filter: Callable[[str], bool] = lambda f : True) -> Iterator[Tuple[uuid.UUID, uuid.UUID]]:
        ...
