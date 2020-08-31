from infrastructure.images import get_ndarray_image, resize_ndarray
## todo: remove infrastructure, allow calling side to supply dependencies

from statistics import mean

from abstractions.recognition import FaceDetector, DistanceEstimator
from abstractions.storages import FeaturesStorage, UsersStorage
from abstractions import User, UserFeatures, Feature, ResizeFactors

import uuid, logging
import datetime

async def handle(
        user_id: uuid.UUID,
        features_storage: FeaturesStorage,
        distance_estimator: DistanceEstimator,
        users_storage: UsersStorage) -> [User]:
    logger = logging.getLogger('use_case__create_or_get_user')


    user_features_input = [feature async for feature in features_storage.enumerate_for(user_id)]
    distances = []

    async for user_features in features_storage.enumerate():

        for user_features_input_feature in user_features_input:
            distances.append(
                (
                    user_features_input_feature.user_id,
                [
                    distance_estimator.distance(
                        [feature.feature for feature in user_features.features],
                        user_input_feature.feature
                    )
                    for user_input_feature in user_features_input_feature.features
                ])
            )
        
    #     current_distances.append({
    #         distance_estimator.distance_vec_to_vec(
    #             [
    #                 feature.feature for feature in user_features_input.features
    #             ], user_features_input.features
    #         )
    #     }


    return distances

    # return closest_user_id
