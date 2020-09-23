from abstractions import User
from abstractions.storages import UsersStorage, ImagesStorage, TransactionContext

from uuid import UUID

async def handle(
        user_id: UUID,
        images_storage: ImagesStorage,
        users_storage: UsersStorage,
        transaction_context: TransactionContext) -> None:
    
    async with transaction_context as scope:
        await images_storage.delete_for_user(person_id=user_id, transaction_scope=scope)
        await users_storage.delete_user(user_id=user_id, transaction_scope=scope)
