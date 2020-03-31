import cv2
import face_recognition
from numpy import ndarray
from abstractions.recognition import FaceDetector

class DlibFaceDetector(FaceDetector):
    def __init__(self):
        pass

    def detect(self, numpy_array: ndarray) -> []:
        image_file = cv2.resize(numpy_array, (0, 0), fx=0.25, fy=0.25)
        rgb_image = image_file[:, :, ::-1]
        return face_recognition.face_locations(rgb_image, 1, 'cnn')
