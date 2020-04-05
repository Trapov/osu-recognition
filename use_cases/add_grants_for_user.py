from abstractions import Page, User
from abstractions.storages import UsersStorage

from uuid import UUID

class UserNotFound(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

async def handle(
        user_id: UUID,
        grant: str,
        users_storage: UsersStorage) -> None:
    
    user : User = await users_storage.single_no_features(user_id=user_id)
    if not user:
        raise UserNotFound()

    user.grants.append(grant)
    await users_storage.save(user=user)