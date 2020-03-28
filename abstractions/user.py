from uuid import UUID
from numpy import ndarray


class User(object):
    def __init__(self, idx: UUID, features_count: int, grants: []):
        self.__id = idx
        self.__features_count = features_count
        self.__grants = grants

    @property
    def idx(self) -> UUID:
        return self.__id

    @property
    def grants(self) -> []:
        return self.__grants

    @property
    def features_count(self) -> int:
        return self.__features_count

