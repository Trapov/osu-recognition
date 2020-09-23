from abstractions.storages import FeaturesStorage, UsersStorage, ImagesStorage, TransactionContext

from datetime import datetime
from uuid import UUID

async def handle(
        user_id: UUID,
        user_id_to: UUID,
        images_storage: ImagesStorage,
        users_storage: UsersStorage,
        features_storage: FeaturesStorage,
        transaction_context: TransactionContext) -> None:
    

    async with transaction_context as scope:
        async for uf in features_storage.enumerate_for(user_id):
            for f in uf.features:
                await features_storage.save(
                    user_id_to, f.idx, f.image_type, f.feature, created_at=datetime.utcnow(),
                    transaction_scope=scope
                )
                
                image = await images_storage.get(user_id, f.idx)
                await images_storage.save(user_id_to, f.image_type, f.idx, image, transaction_scope=scope)
        
        await users_storage.delete_user(user_id, transaction_scope=scope)