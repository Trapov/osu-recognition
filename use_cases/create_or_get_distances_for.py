from infrastructure.images import get_ndarray_image, resize_ndarray
## todo: remove infrastructure, allow calling side to supply dependencies

from abstractions.recognition import FaceDetector, DistanceEstimator
from abstractions.storages import FeaturesStorage, UsersStorage
from abstractions import UserFeatures, Feature, ResizeFactors

import uuid, logging
import datetime
import statistics

async def handle(
        user_id: uuid.UUID,
        features_storage: FeaturesStorage,
        distance_estimator: DistanceEstimator,
        users_storage: UsersStorage) -> []:
    logger = logging.getLogger('use_case__create_or_get_distances_for')


    user_features_input = [
        item for sublist in [
            n.features async for n in features_storage.enumerate_for(user_id)
        ] for item in sublist
    ]    
    
    distances = {}

    #todo: only 10 max users

    async for user_features in features_storage.enumerate():

        if user_features.user_id == user_id:
            continue

        for user_input_feature in user_features_input:
            dists = {
                str(user_input_feature.image_name) : { 
                    str(feature.image_name) : distance.tolist() for (feature, distance) in zip(
                        user_features.features, distance_estimator.distance(
                            [feature.feature for feature in user_features.features],
                            user_input_feature.feature
                        )
                    )
                }
            }

            distances.setdefault(str(user_features.user_id), {}).update(dists)
    

    distances = [
        { 
            "user_id": idx,
            "features": [
                { 
                    "feature_id_from" : feature_id,
                    "features_to":  [
                        { 
                             "feature_id_to" : feature_id_to, 
                             "distance": distances[idx][feature_id][feature_id_to] 
                        }  for feature_id_to in distances[idx][feature_id] 
                    ]
                } for feature_id in distances[idx]
            ] 
        } for idx in distances
    ]

    distances = [
        { 
            "user_id": user["user_id"],
            "features": [
                { 
                    "feature_id_from" : feature_from["feature_id_from"],
                    "distance": statistics.median([ft["distance"] for ft in feature_from["features_to"]]),
                    "features_to":  [
                        { 
                             "feature_id_to" : feature_to["feature_id_to"],
                             "distance": feature_to["distance"],
                        } for feature_to in feature_from["features_to"]
                    ]
                } for feature_from in user['features']
            ] 
        } for user in distances
    ]

    distances = [d for d in sorted([
        { 
            "user_id": user["user_id"],
            "distance": statistics.median([us["distance"] for us in user["features"]]),
            "features": [
                { 
                    "feature_id_from" : feature_from["feature_id_from"],
                    "distance": feature_from["distance"],
                    "features_to":  [
                        { 
                             "feature_id_to" : feature_to["feature_id_to"],
                             "distance": feature_to["distance"],
                        } for feature_to in sorted(feature_from["features_to"], key=lambda x : x["distance"], reverse=False)
                    ]
                } for feature_from in sorted(user['features'], key=lambda x: x["distance"], reverse=False)
            ]
        } for user in distances
    ], key=lambda x: x["distance"], reverse=False)]

    return distances