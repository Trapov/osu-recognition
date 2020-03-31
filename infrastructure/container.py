from abstractions.recognition import FaceDetector, FeatureExtractor, DistanceEstimator
from abstractions import GrantsCrypto

import logging

from .recognition import DlibFaceDetector, DlibFeatureExtractor, NumpyDistanceEstimator
from .jwt_grants_crypto import JwtGrantsCrypto
from abstractions.storages import FeaturesStorage, GrantsStorage, ImagesStorage
from infrastructure.storages import FileFeaturesStorage, FileGrantsStorage, FileImagesStorage
from infrastructure.recognition import NumpyDistanceEstimator


class ServicesContainer(object):
    def __init__(self):
        self.detector : FaceDetector = DlibFaceDetector()
        self.extractor : FeatureExtractor = DlibFeatureExtractor()
        self.grants_crypto : GrantsCrypto = JwtGrantsCrypto(secret_key='ada wong')
        
        # self.storage : PersonsStorage = FileStorage(imgs_directory='images', features_directory='features', features_threshold= 0.2)

        self.features_storage : FeaturesStorage = FileFeaturesStorage('features')
        self.grants_storage : GrantsStorage =  FileGrantsStorage('grants')
        self.images_storage : ImagesStorage = FileImagesStorage('images')

        self.distance_estimator : DistanceEstimator = NumpyDistanceEstimator()

SINGLETON_CONTAINER = ServicesContainer()