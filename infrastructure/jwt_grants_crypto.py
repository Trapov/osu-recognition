from abstractions import GrantsCrypto
from typing import List
from uuid import UUID
import jwt
import datetime


class JwtGrantsCrypto(GrantsCrypto):
    def __init__(self, secret_key: str):
        self.__secret_key = secret_key

    def to_token(self, person_id: UUID, grants: List[str]) -> str:
        return jwt.encode({
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
            'sub': str(person_id),
            'grants': grants
        }, self.__secret_key, algorithm='HS256')
