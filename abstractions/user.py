from uuid import UUID
from numpy import ndarray
from typing import List

class Feauture(object):
    def __init__(self, idx: UUID, image_name : str):
        self.__idx = idx
        self.__image_name = image_name

    @property
    def idx(self) -> UUID:
        return self.__idx

    @property
    def image_name(self) -> str:
        return self.__image_name

class UserFeatures(object):
    def __init__(self, features : List[Feauture]):
        self.__count = len(features)
        self.__features = features

    @property
    def features(self) -> List[Feauture]:
        return self.__features

    @property
    def count(self) -> int:
        return self.__count

class User(object):
    def __init__(self, idx: UUID, user_features: UserFeatures, grants: []):
        self.__id = idx
        self.__grants = grants
        self.__features = user_features

    @property
    def idx(self) -> UUID:
        return self.__id

    @property
    def grants(self) -> []:
        return self.__grants

    @property
    def features(self) -> UserFeatures:
        return self.__features