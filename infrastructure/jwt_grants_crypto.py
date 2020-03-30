from abstractions import GrantsCrypto
from typing import List
from uuid import UUID
import jwt

class JwtGrantsCrypto(GrantsCrypto):
    def __init__(self, secret_key : str):
        self.__secret_key = secret_key

    def to_token(self, person_id: UUID, grants : List[str]) -> str:
        return jwt.encode( {
            'user_id' : str(person_id),
            'grants' : grants
        }, self.__secret_key, algorithm='HS256')
