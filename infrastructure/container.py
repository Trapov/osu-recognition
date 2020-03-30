from abstractions.recognition import FaceDetector, FeatureExtractor
from abstractions import PersonsStorage

import logging

from .recognition import DlibFaceDetector
from .recognition import DlibFeatureExtractor
from .storages import FileStorage

class ServicesContainer(object):
    def __init__(self):
        self.detector : FaceDetector = DlibFaceDetector()
        self.extractor : FeatureExtractor = DlibFeatureExtractor()
        self.storage : PersonsStorage = FileStorage('features', 0.2)

SINGLETON_CONTAINER = ServicesContainer()