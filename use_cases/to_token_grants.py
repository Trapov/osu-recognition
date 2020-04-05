from abstractions import GrantsCrypto, User
from abstractions.storages import UsersStorage
from uuid import UUID


class NoGrantsFound(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


async def handle(user_id: UUID, users_storage: UsersStorage, grants_crypto: GrantsCrypto) -> str:
    user : User = await users_storage.single_no_features(user_id=user_id)

    if not user:
        raise NoGrantsFound()

    return grants_crypto.to_token(user.idx, list(user.grants))
