from abstractions import User
from abstractions.storages import UsersStorage, ImagesStorage

from uuid import UUID

async def handle(
        user_id: UUID,
        images_storage: ImagesStorage,
        users_storage: UsersStorage) -> None:
    
    #todo: in one transaction
    await images_storage.delete_for_user(person_id=user_id)
    await users_storage.delete_user(user_id=user_id)
