from abstractions.storages import FeaturesStorage, UsersStorage, ImagesStorage, TransactionContext

from datetime import datetime
from uuid import UUID, uuid4

async def handle(
        user_id: UUID,
        feature_id: UUID,
        user_id_to: UUID,
        images_storage: ImagesStorage,
        users_storage: UsersStorage,
        features_storage: FeaturesStorage,
        transaction_context: TransactionContext) -> None:
    
    user_features = [
        item for sublist in [
            n.features async for n in features_storage.enumerate_for(user_id)
        ] for item in sublist
    ]

    if len(user_features) == 1:
        raise Exception("Cannot delete last feature. Use delete user instead.")

    feature = [ n for n in user_features if n.idx == feature_id][0]

    async with transaction_context as scope:
        await features_storage.save(user_id_to, feature.idx, feature.image_type, feature.feature, datetime.utcnow(), transaction_scope=scope)

        await features_storage.delete(user_id, feature.idx, transaction_scope=scope)
        img = await images_storage.get(user_id, feature.idx)

        await images_storage.save(user_id_to, feature.image_type, feature.idx, img, transaction_scope=scope) 
        await images_storage.delete(user_id, feature.idx, transaction_scope=scope)