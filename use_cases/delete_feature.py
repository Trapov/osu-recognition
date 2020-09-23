from abstractions.storages import FeaturesStorage, ImagesStorage, TransactionContext

from uuid import UUID

async def handle(
        user_id: UUID,
        feature_id: UUID,
        images_storage: ImagesStorage,
        features_storage: FeaturesStorage,
        transaction_context: TransactionContext) -> None:
    
    if len([item for sublist in [n.features async for n in features_storage.enumerate_for(user_id)] for item in sublist]) == 1:
        raise Exception("Cannot delete last feature. Use delete user instead.")

    async with transaction_context as scope:
        await images_storage.delete(person_id=user_id, feature_id=feature_id, transaction_scope=scope)
        await features_storage.delete(user_id=user_id, idx=feature_id, transaction_scope= scope)
