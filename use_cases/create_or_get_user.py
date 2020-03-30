from infrastructure.storages import FileStorage, User
from infrastructure.container import ServicesContainer
from infrastructure.images import get_ndarray_image
import uuid, logging

def handle(image_bytes: bytes, container: ServicesContainer) -> User:
    image_byte_array = get_ndarray_image(image_bytes)
    faces = container.detector.detect(image_byte_array)
    if len(faces) == 0:
        raise Exception("No faces found")
    features = container.extractor.extract(image_byte_array, faces)
    if len(features) == 0:
        raise Exception("Not features available for the face")

    feature = next(f for f in features)
    user = container.storage.neareset(feature=feature)
    feature_vector_idx = uuid.uuid4()

    if user: 
        
        if user.features_count < 10:
            logging.debug(f'Saving user [{user.idx}] features with idx [{feature_vector_idx}]')
            container.storage.save(user.idx, feature_vector_idx, feature)
        
        return user

    idx = uuid.uuid4()
    logging.debug(f'Saving new user [{user.idx}] features with idx [{feature_vector_idx}]')
    container.storage.save(idx, feature_vector_idx, feature)
    user = User(idx, 1, [])

    return user