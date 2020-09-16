from infrastructure.images import get_ndarray_image, resize_ndarray
## todo: remove infrastructure, allow calling side to supply dependencies

from abstractions.recognition import FaceDetector, DistanceEstimator
from abstractions.storages import FeaturesStorage, UsersStorage
from abstractions import UserFeatures, Feature, ResizeFactors

import uuid, logging
import datetime

async def handle(
        user_id: uuid.UUID,
        features_storage: FeaturesStorage,
        distance_estimator: DistanceEstimator,
        users_storage: UsersStorage) -> []:
    logger = logging.getLogger('use_case__create_or_get_distances_for')


    user_features_input = [feature async for feature in features_storage.enumerate_for(user_id)]
    distances = {}

    async for user_features in features_storage.enumerate():

        if user_features.user_id == user_id:
            continue

        for user_features_input_feature in user_features_input:
            dists = {
                str(user_input_feature.image_name) : { 
                    str(feature.image_name) : distance.tolist() for (feature, distance) in zip(
                        user_features.features, distance_estimator.distance(
                            [feature.feature for feature in user_features.features],
                            user_input_feature.feature
                        )
                    )
                }
                for user_input_feature in user_features_input_feature.features
            }

            distances.setdefault(str(user_features.user_id), {}).update(dists)
        
    return distances

    # return closest_user_id
