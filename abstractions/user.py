from uuid import UUID
from numpy import ndarray
from typing import List
from datetime import datetime

class Feature(object):
    def __init__(self, idx: UUID, image_type: str, created_at: datetime, feature: bytes):
        self.__idx = idx
        self.__image_type = image_type
        self.__created_at = created_at
        self.__feature = feature

    @property
    def idx(self) -> UUID:
        return self.__idx

    @property
    def image_type(self) -> str:
        return self.__image_type

    @property
    def image_name(self) -> str:
        return f'{self.__idx}.{self.__image_type}'

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @property
    def feature(self) -> bytes:
        return self.__feature

class UserFeatures(object):
    def __init__(self, user_id: UUID, features: List[Feature]):
        self.__user_id = user_id
        self.__features = features

    @property
    def user_id(self) -> UUID:
        return self.__user_id

    @property
    def features(self) -> List[Feature]:
        return self.__features

    @property
    def count(self) -> int:
        return len(self.__features)


class User(object):
    def __init__(self, idx: UUID, user_features: UserFeatures, grants: [], created_at: datetime):
        self.__id = idx
        self.__grants = grants
        self.__created_at: datetime = created_at
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

    @property
    def created_at(self) -> datetime:
        return self.__created_at