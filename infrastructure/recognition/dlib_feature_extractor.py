import face_recognition
from numpy import ndarray
from abstractions.recognition import FeatureExtractor

class DlibFeatureExtractor(FeatureExtractor):
    def __init__(self):
        pass

    def extract(self, numpy_array: ndarray, faces: []) -> []:
        return face_recognition.face_encodings(numpy_array, faces)