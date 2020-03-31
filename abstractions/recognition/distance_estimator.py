from abc import ABC, abstractmethod
from typing import List


class DistanceEstimator(ABC):
    @abstractmethod
    def distance(self, face_features_we_have : List[bytes], face_feature_to_compare: List[float]) -> List[float]:
        ...
