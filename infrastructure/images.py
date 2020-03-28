from PIL import Image

import base64, io, numpy

def get_ndarray_image(img_bytes: bytes) -> numpy.ndarray:
    return numpy.array(__pil_image_from_bytes(img_bytes))[:, :, ::-1]


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
