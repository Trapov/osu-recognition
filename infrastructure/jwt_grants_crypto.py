from abstractions import GrantsCrypto
from typing import List, Tuple
from uuid import UUID
import jwt
import datetime


class JwtGrantsCrypto(GrantsCrypto):
    def __init__(self, secret_key: str):
        self.__secret_key = secret_key

    def to_token(self, person_id: UUID, grants: List[str]) -> str:
        return jwt.encode({
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            'sub': str(person_id),
            'grants': grants
        }, self.__secret_key, algorithm='HS256')

    def to_user_id_with_grants(self, token: str) -> Tuple[UUID, List[str]]:
        decoded = jwt.decode(jwt=token, key=self.__secret_key, verify=True, algorithms=['HS256'])
        return (decoded['sub'], decoded['grants'])