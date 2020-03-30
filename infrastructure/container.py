from abstractions.recognition import FaceDetector, FeatureExtractor
from abstractions import PersonsStorage, GrantsCrypto

import logging

from .recognition import DlibFaceDetector
from .recognition import DlibFeatureExtractor
from .storages import FileStorage
from .jwt_grants_crypto import JwtGrantsCrypto

class ServicesContainer(object):
    def __init__(self):
        self.detector : FaceDetector = DlibFaceDetector()
        self.extractor : FeatureExtractor = DlibFeatureExtractor()
        self.grants_crypto : GrantsCrypto = JwtGrantsCrypto(secret_key='ada wong')
        self.storage : PersonsStorage = FileStorage(imgs_directory='images', features_directory='features', features_threshold= 0.2)

SINGLETON_CONTAINER = ServicesContainer()