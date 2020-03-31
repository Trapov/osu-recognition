import cv2
import face_recognition
from numpy import ndarray
from abstractions.recognition import FaceDetector
from typing import Tuple, List

class DlibFaceDetector(FaceDetector):
    def __init__(self):
        pass

    def detect(self, numpy_array: ndarray) -> List[float]:
        return face_recognition.face_locations(numpy_array, 1, 'cnn')
