from abc import ABC, abstractmethod
from numpy import ndarray

class FeatureExtractor(ABC):
    @abstractmethod
    def extract(self, numpy_array: ndarray, faces: []) -> []:
        ...
