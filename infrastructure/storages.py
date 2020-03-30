from typing import Union, List, Tuple

from abstractions import User, PersonsStorage
import numpy as np
from uuid import UUID
import os, aiofiles

import face_recognition

class FileStorage(PersonsStorage):
    def __init__(self, features_directory: str, imgs_directory: str, features_threshold: int = 0.5):
        self.__features_threshold = features_threshold
        self.__features_directory = self.__create_if_not_exists(features_directory)
        self.__imgs_directory = self.__create_if_not_exists(imgs_directory)

    async def save(self, person_id: UUID, idx: UUID, feature: np.ndarray, img: bytes, image_type: str = "jpg",) -> None:
        features_directory = self.__create_if_not_exists(os.path.join(self.__features_directory, str(person_id)))
        imgs_directory = self.__create_if_not_exists(os.path.join(self.__imgs_directory, str(person_id)))

        async with aiofiles.open(os.path.join(imgs_directory, str(idx)) + f'.{image_type}', 'wb+') as f:
            await f.write(img)

        async with aiofiles.open(os.path.join(features_directory, str(idx)), 'wb+') as f:
            await f.write(feature.tobytes())

    async def paged_users(self) -> List[User]:
        for directory in os.listdir(self.__features_directory):
            person_features = []
            person_path = os.path.join(self.__features_directory, directory)

            for file_name in os.listdir(person_path):
                try:
                    if UUID(file_name):
                        person_features.append(file_name)    
                except:
                    pass
            
            features_count = len(person_features)

            try :
                async with aiofiles.open(os.path.join(person_path, 'grants.txt')) as grants_file:
                    yield User(UUID(directory), features_count, await grants_file.readlines())
            except:
                yield User(UUID(directory), features_count, [])

        
    async def neareset(self, feature: []) -> Union[Tuple[User, float], None]:
        person_distances = []
        for directory in os.listdir(self.__features_directory):
            person_features = []
            person_path = os.path.join(self.__features_directory, directory)
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
            async with aiofiles.open(os.path.join(self.__features_directory, person_distance['idx'], 'grants.txt'), 'r') as fp:
                return (User(person_distance['idx'], person_distance['person_features_count'], await fp.readlines()), person_distance['distance'])
        except FileNotFoundError as ex:
            return (User(person_distance['idx'], person_distance['person_features_count'], []), person_distance['distance'])

    async def get_grants(self, person_id: UUID) -> []:
        try:
            async with aiofiles.open(os.path.join(self.__features_directory, str(person_id), 'grants.txt'), 'r') as fp:
                return await fp.readlines()
        except:
            return []
        return []

    @staticmethod
    def __create_if_not_exists(directory: str) -> str:
        if not os.path.exists(directory):
            os.mkdir(directory)
        
        return directory
