from infrastructure.storages import FileStorage, User
from infrastructure.container import ServicesContainer
from infrastructure.images import get_ndarray_image
## todo: remove infrastructure, allow calling side to supply dependencies

import uuid, logging

class InputImage:
    def __init__(self, image_bytes : bytes, image_type: str = "jpg"):
        self.bytes = image_bytes
        self.type = image_type

async def handle(input_image : InputImage, container: ServicesContainer) -> User:
    image_bytes = input_image.bytes
    image_byte_array = get_ndarray_image(image_bytes)
    faces = container.detector.detect(image_byte_array)
    if len(faces) == 0:
        raise Exception("No faces found")
    features = container.extractor.extract(image_byte_array, faces)
    if len(features) == 0:
        raise Exception("Not features available for the face")

    feature = next(f for f in features)
    (user, distance) = await container.storage.neareset(feature=feature)
    feature_vector_idx = uuid.uuid4()

    if user: 
        
        if user.features_count < 10 and distance > 0.0:
            logging.debug(f'Saving user [{user.idx}] features with idx [{feature_vector_idx}]')
            await container.storage.save(user.idx, feature_vector_idx, feature, image_bytes, input_image.type)
        
            return User(user.idx, user.features_count + 1, user.grants)

        return User(user.idx, user.features_count, user.grants)

    idx = uuid.uuid4()
    user = User(idx, 1, [])
    logging.debug(f'Saving new user [{user.idx}] features with idx [{feature_vector_idx}]')
    await container.storage.save(idx, feature_vector_idx, feature, image_bytes)

    return user