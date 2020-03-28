from abc import ABC, abstractmethod
from numpy import ndarray

class FaceDetector(ABC):
    @abstractmethod
    def detect(self, numpy_array: ndarray) -> []:
        ...
