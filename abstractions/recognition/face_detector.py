from abc import ABC, abstractmethod
from typing import Tuple, List
from numpy import ndarray

class FaceDetector(ABC):
    @abstractmethod
    def detect(self, numpy_array: ndarray) -> List[float]:
        ...
