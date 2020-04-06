from infrastructure.images import get_ndarray_image, resize_ndarray
## todo: remove infrastructure, allow calling side to supply dependencies

from statistics import mean

from abstractions.recognition import FaceDetector, FeatureExtractor, DistanceEstimator
from abstractions.storages import FeaturesStorage, ImagesStorage, UsersStorage
from abstractions import User, UserFeatures, Feature

import uuid, logging
import datetime


class InputImage:
    def __init__(self, image_bytes: bytes, image_type: str = "jpg"):
        self.bytes = image_bytes
        self.type = image_type


class NoFacesFound(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NoFeaturesExtracted(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


async def handle(
        input_image: InputImage,
        face_detector: FaceDetector,
        feature_extractor: FeatureExtractor,
        features_storage: FeaturesStorage,
        distance_estimator: DistanceEstimator,
        users_storage: UsersStorage,
        images_storage: ImagesStorage) -> uuid.UUID:
    logger = logging.getLogger('use_case__create_or_get_user')
    ndarray_resized = resize_ndarray(get_ndarray_image(input_image.bytes), (0.3, 0.3))

    logger.debug('Detecting faces.')

    detected_face_bboxes: [] = face_detector.detect(ndarray_resized)

    if len(detected_face_bboxes) == 0:
        raise NoFacesFound()

    logger.debug('Extracting features.')

    extracted_features: [] = next(
        iter(feature_extractor.extract(ndarray_resized, detected_face_bboxes)), []
    )

    if len(extracted_features) == 0:
        raise NoFeaturesExtracted()

    logger.debug('Estimating distances')
    closest_user_id, distance_to_closest_user, number_of_features = None, None, None
    async for user_features in features_storage.enumerate():

        current_user_id = user_features.user_id
        current_distances = distance_estimator.distance([feature.feature for feature in user_features.features], extracted_features)

        if 0.0 in current_distances:
            logger.info(f'Found user with ZERO distance. [{current_user_id}]')
            return current_user_id

        avg_distance_of_user = mean(current_distances)

        if not distance_to_closest_user:
            closest_user_id, distance_to_closest_user, number_of_features = current_user_id, avg_distance_of_user, len(
                current_distances)
        elif avg_distance_of_user < distance_to_closest_user:
            closest_user_id, distance_to_closest_user, number_of_features = current_user_id, avg_distance_of_user, len(
                current_distances)

    if closest_user_id:
        logger.info(f'Distance to user[{closest_user_id}] = [{distance_to_closest_user}]')
        threshold = 0.64 - (0.03 * number_of_features)
        logger.info(f'Current threshold [{threshold}]')

        if number_of_features < 11 and distance_to_closest_user <= threshold:
            feature_id = uuid.uuid4()

            await users_storage.save(
                User(
                    idx=closest_user_id,
                    user_features=UserFeatures(
                        closest_user_id, features=[
                            Feature(
                                idx=feature_id,
                                image_type=input_image.type,
                                created_at=datetime.datetime.utcnow(),
                                feature=extracted_features.tobytes())
                        ]),
                        grants=[],
                        created_at=datetime.datetime.utcnow()
                )
            )
            
            await images_storage.save(closest_user_id, input_image.type, feature_id, input_image.bytes)

            return closest_user_id

    feature_id = uuid.uuid4()
    closest_user_id = uuid.uuid4()
    await users_storage.save(
        User(
            idx=closest_user_id,
            user_features=UserFeatures(
                closest_user_id, features=[
                    Feature(
                        idx=feature_id,
                        image_type=input_image.type,
                        created_at=datetime.datetime.utcnow(),
                        feature=extracted_features.tobytes())
                ]),
            grants=[],
            created_at=datetime.datetime.utcnow()
        )
    )
    await images_storage.save(closest_user_id, input_image.type, feature_id, input_image.bytes)

    return closest_user_id
