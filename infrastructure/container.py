from abstractions import GrantsCrypto
from abstractions.recognition import FaceDetector, FeatureExtractor, DistanceEstimator
from abstractions.storages import FeaturesStorage, ImagesStorage, UsersStorage

from .jwt_grants_crypto import JwtGrantsCrypto
from .recognition import DlibFaceDetector, DlibFeatureExtractor, NumpyDistanceEstimator
from .storages import SqliteFeaturesStorage, SqliteUsersStorage, FileImagesStorage


class ServicesContainer(object):
    def __init__(self):
        self.detector: FaceDetector = DlibFaceDetector()
        self.extractor: FeatureExtractor = DlibFeatureExtractor()
        self.grants_crypto: GrantsCrypto = JwtGrantsCrypto(secret_key='ada wong')

        self.users_storage: UsersStorage = SqliteUsersStorage('osu_recognition.db')
        self.features_storage: FeaturesStorage = SqliteFeaturesStorage('osu_recognition.db')
        self.images_storage: ImagesStorage = FileImagesStorage('images')

        self.distance_estimator: DistanceEstimator = NumpyDistanceEstimator()


SINGLETON_CONTAINER = ServicesContainer()
