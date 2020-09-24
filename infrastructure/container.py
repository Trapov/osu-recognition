from abstractions import GrantsCrypto
from abstractions.recognition import FaceDetector, FeatureExtractor, DistanceEstimator
from abstractions.storages import FeaturesStorage, ImagesStorage, UsersStorage, TransactionContext, RecognitionSettingsStorage

from .jwt_grants_crypto import JwtGrantsCrypto
from .recognition import DlibFaceDetector, DlibFeatureExtractor, NumpyDistanceEstimator
from .storages import SqliteFeaturesStorage, SqliteImagesStorage, SqliteUsersStorage, AiosqliteTransactionContext, SqliteRecognitionSettingsStorage


class ServicesContainer(object):
    def __init__(self):
        self.detector: FaceDetector = DlibFaceDetector()
        self.extractor: FeatureExtractor = DlibFeatureExtractor()
        self.grants_crypto: GrantsCrypto = JwtGrantsCrypto(secret_key='ada wong')

        self.__register_storages_sqlite()
    
        self.distance_estimator: DistanceEstimator = NumpyDistanceEstimator()


    def __register_storages_sqlite(self) -> None:
        self.transaction_context_factory : TransactionContext = lambda : AiosqliteTransactionContext('osu_recognition.db')
        self.users_storage: UsersStorage = SqliteUsersStorage('osu_recognition.db')
        self.recognition_settings_storage : RecognitionSettingsStorage = SqliteRecognitionSettingsStorage('osu_recognition.db')
        self.features_storage: FeaturesStorage = SqliteFeaturesStorage('osu_recognition.db')
        self.images_storage: ImagesStorage = SqliteImagesStorage('osu_recognition.db') #FileImagesStorage('images')


SINGLETON_CONTAINER = ServicesContainer()
