from PIL import Image
from typing import Tuple
import base64, io, numpy, cv2

def get_ndarray_image(img_bytes: bytes) -> numpy.ndarray:
    return numpy.array(__pil_image_from_bytes(img_bytes))[:, :, ::-1]

def resize_ndarray(numpy_array: numpy.ndarray, x_y_factors : Tuple[float, float] = (0.25, 0.25)) -> numpy.ndarray:
    (fx, fy) = x_y_factors
    image_file = cv2.resize(numpy_array, (0, 0), fx=fx, fy=fy)
    return image_file[:, :, ::-1]

def get_image_bytes_from_base_64(base_64_string: str) -> []:
    return base64.b64decode(
        base_64_string\
            .split(',')[1]\
            .encode()
    )


def __pil_image_from_bytes(img_bytes: bytes) -> Image.Image:
    return Image\
        .open(io.BytesIO(img_bytes))\
        .convert('RGB')
