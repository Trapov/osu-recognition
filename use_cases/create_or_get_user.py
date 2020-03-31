from infrastructure.container import ServicesContainer
from infrastructure.images import get_ndarray_image, resize_ndarray
## todo: remove infrastructure, allow calling side to supply dependencies

from statistics import mean

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
    ndarray_resized = resize_ndarray(get_ndarray_image(input_image.bytes))
    
    logger.debug('Detecting faces.')

    detected_face_bboxes : [] = face_detector.detect(ndarray_resized)

    if len(detected_face_bboxes) == 0:
        raise NoFacesFound()

    logger.debug('Extracting features.')

    extracted_features : [] = next(
        iter(feature_extractor.extract(ndarray_resized, detected_face_bboxes)), []
    )

    if len(extracted_features) == 0:
        raise NoFeaturesExtracted()

    
    features : List[PersonFeatures] = [
        feature 
        async for feature in features_storage.enumerate()
    ]
    
    logger.debug('Estimating distances')

    estimated_distances_for_persons = [
        (person_features.person_id, distance_estimator.distance([feature.feature for feature in person_features.features], extracted_features))
        for person_features in features
    ]

    zero_distance_persone = next((f for f in estimated_distances_for_persons if len(list(dist for dist in f[1] if dist == 0.0)) > 0), None)

    if zero_distance_persone:
        logger.debug(f'Found person with ZERO distance. [{zero_distance_persone[0]}]')
        return zero_distance_persone[0]


    (person_id, min_distance) = next(
        iter(
            sorted(
            [
                (person_features[0], mean(person_features[1]))
                for person_features in estimated_distances_for_persons
            ], key=lambda t : t[1])
        ),
        (None, None)
    )


    if person_id:
        logger.debug(f'Distance to person[{person_id}] = [{min_distance}]')
        number_of_features = len(next(f for f in features if f.person_id == person_id).features)
        threshold = 0.5 - (0.03 * number_of_features)
        logger.debug(f'Current threshold [{threshold}]')

        if number_of_features < 11 and min_distance <= threshold:
            feature_id = uuid.uuid4()
            await features_storage.save(person_id, feature_id, extracted_features.tobytes())
            await images_storage.save(person_id, input_image.type, feature_id, input_image.bytes)
            
            return person_id


    feature_id = uuid.uuid4()
    person_id = uuid.uuid4()
    await features_storage.save(person_id, feature_id, extracted_features.tobytes())
    await images_storage.save(person_id, input_image.type, feature_id, input_image.bytes)

    return person_id