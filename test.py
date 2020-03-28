# import face_recognition, time, cv2

# start_time = time.time()
# image_file = face_recognition.load_image_file("hex.png")
# image_file = cv2.resize(image_file, (0, 0), fx=0.25, fy=0.25)
# rgb_image_file = image_file[:, :, ::-1]

# face_locations : list = face_recognition.face_locations(rgb_image_file, 1, 'cnn')
# print(face_locations)
# feature_vector = face_recognition.face_encodings(rgb_image_file, face_locations)[0]
# print(feature_vector)
# obama_image = face_recognition.load_image_file("D:/rayso/Pictures/600px-Forsennew.jpg")
# obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# distance = face_recognition.face_distance([feature_vector], obama_face_encoding)
# print(distance)
# print(time.time() - start_time)

import dependency_injector
from dependency_injector.providers import BaseSingleton
print(type(dependency_injector.__version__).__name__)
