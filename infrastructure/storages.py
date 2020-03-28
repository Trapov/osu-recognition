from typing import Union, List

from abstractions import User, PersonsStorage
import numpy as np
from uuid import UUID
import os

import face_recognition

class FileStorage(PersonsStorage):
    def __init__(self, directory: str, features_threshold: int = 0.5):
        self.__features_threshold = features_threshold
        self.__directory = self.__create_if_not_exists(directory)

    def save(self, person_id: UUID, idx: UUID, feature: np.ndarray) -> None:
        directory = self.__create_if_not_exists(os.path.join(self.__directory, str(person_id)))
        with open(os.path.join(directory, str(idx)), 'wb+') as f:
            f.write(feature.tobytes())

    def paged_users(self) -> List[User]:
        for directory in os.listdir(self.__directory):
            person_features = []
            person_path = os.path.join(self.__directory, directory)

            for file_name in os.listdir(person_path):
                try:
                    if UUID(file_name):
                        person_features.append(file_name)    
                except:
                    pass
            
            features_count = len(person_features)

            try :
                with open(os.path.join(person_path, 'grants.txt')) as grants_file:
                    yield User(UUID(directory), features_count, grants_file.readlines())
            except:
                yield User(UUID(directory), features_count, [])

        
    def neareset(self, feature: []) -> Union[User, None]:
        person_distances = []
        for directory in os.listdir(self.__directory):
            person_features = []
            person_path = os.path.join(self.__directory, directory)
            for file_name in os.listdir(person_path):
                try:
                    if UUID(file_name):
                        person_features.append(np.fromfile(os.path.join(person_path, file_name)))
                except:
                    pass

            person_features_count = len(person_features)

            distance = face_recognition.face_distance(person_features, feature)
            person_distances.append({
                'idx': directory,
                'person_features_count': person_features_count,
                'distance': distance[0]
            })

        person_distance = (min(person_distances, key=lambda x: x['distance']) if len(person_distances) > 0 else None)
        if person_distance is None or person_distance['distance'] > self.__features_threshold:
            return None

        try:
            with open(os.path.join(self.__directory, person_distance['idx'], 'grants.txt'), 'r') as fp:
                return User(person_distance['idx'], person_distance['person_features_count'], fp.readlines())
        except FileNotFoundError as ex:
            return User(person_distance['idx'], person_distance['person_features_count'], [])

    @staticmethod
    def __create_if_not_exists(directory: str) -> str:
        if not os.path.exists(directory):
            os.mkdir(directory)

        return directory
