from infrastructure.container import ServicesContainer
from infrastructure.images import get_ndarray_image
## todo: remove infrastructure, allow calling side to supply dependencies

from abstractions.recognition import FaceDetector, FeatureExtractor, DistanceEstimator
from abstractions.storages import FeaturesStorage, ImagesStorage, PersonFeatures
from typing import List, Iterator

import uuid, logging

class InputImage:
    def __init__(self, image_bytes : bytes, image_type: str = "jpg"):
        self.bytes = image_bytes
        self.type = image_type

class NoFacesFound(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NoFeaturesExtracted(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

async def handle(
    input_image : InputImage,
    face_detector: FaceDetector,
    feature_extractor: FeatureExtractor,
    features_storage: FeaturesStorage,
    distance_estimator : DistanceEstimator,
    images_storage: ImagesStorage) -> uuid.UUID:
    
    logger = logging.getLogger('use_case__create_or_get_user')

    ndarray = get_ndarray_image(input_image.bytes)
    detected_face_bboxes : [] = face_detector.detect(ndarray)

    if len(detected_face_bboxes) == 0:
        raise NoFacesFound()

    extracted_features : [] = next(
        iter(feature_extractor.extract(ndarray, detected_face_bboxes)), []
    )

    if len(extracted_features) == 0:
        raise NoFeaturesExtracted()

    features : List[PersonFeatures] = [feature async for feature in features_storage.enumerate()]

    (person_id, min_distance) = next(
        iter(
            sorted(
            [
                (person_features.person_id, min(distance_estimator.distance([feature.feature for feature in person_features.features], extracted_features)))
                for person_features in features
            ], key=lambda t : t[1])
        ),
        (None, None)
    )

    if person_id and min_distance:
        logger.info(f'Distance to person[{person_id}] = [{min_distance}]')

    if person_id and min_distance < 0.2:
        if len(next(f for f in features if f.person_id == person_id).features) < 10 and min_distance > 0.0:
            feature_id = uuid.uuid4()
            await features_storage.save(person_id, feature_id, extracted_features.tobytes())
            await images_storage.save(person_id, input_image.type, feature_id, input_image.bytes)
        
        return person_id

    feature_id = uuid.uuid4()
    person_id = uuid.uuid4()
    await features_storage.save(person_id, feature_id, extracted_features.tobytes())
    await images_storage.save(person_id, input_image.type, feature_id, input_image.bytes)

    return person_id