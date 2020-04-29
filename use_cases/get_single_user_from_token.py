from abstractions import GrantsCrypto, User
from abstractions.storages import UsersStorage
from uuid import UUID


class NoUserFound(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


async def handle(token: str, users_storage: UsersStorage, grants_crypto: GrantsCrypto) -> User:
    user_id, grants = grants_crypto.to_user_id_with_grants(token)
    user : User = await users_storage.single_no_features(user_id=user_id)

    if not user:
        raise NoUserFound()

    return user

