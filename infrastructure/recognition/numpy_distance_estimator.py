# from __future__ import absolute_import
from abstractions.recognition import DistanceEstimator
import numpy
from typing import List

class NumpyDistanceEstimator(DistanceEstimator):
    def distance(self, face_features_we_have : List[bytes], face_feature_to_compare: []) -> List[float]:
        if len(face_features_we_have) == 0:
            return numpy.empty((0))

        array_we_have = [numpy.frombuffer(face_feature_we_have, dtype=float) for face_feature_we_have in face_features_we_have]

        diff_result = numpy.asfarray(array_we_have) - face_feature_to_compare

        return numpy.linalg.norm(diff_result,  axis=1)
