import aiofiles, uuid
from typing import List, Tuple, Callable, Iterator
from aiofiles.base import AiofilesContextManager
import os
import asyncio

from abstractions.storages import PersonFeatures, Feature, FeaturesStorage

class FileFeaturesStorage(FeaturesStorage):
    def __init__(self, directory : str):
        self.__directory : str = directory

    async def save(self, person_id: uuid.UUID, feature_id: uuid.UUID, feature: bytes) -> None:
        person_directory = self.__create_if_not_exists(self.__add_base_path_to_path(str(person_id)))
        full_feature_path = os.path.join(person_directory, str(feature_id))

        async with aiofiles.open(file=full_feature_path, mode='wb') as fp:
            await fp.write(feature)


    async def enumerate(self, persons_filter: Callable[[str], bool] = lambda f : True) -> Iterator[PersonFeatures]:
        if not os.path.exists(self.__directory):
            return
        
        for person_directory in map(self.__add_base_path_to_path, filter(persons_filter, filter(self.__is_uuid, os.listdir(self.__directory)))):
            yield PersonFeatures(
                person_id=self.__last_path_to_uuid(person_directory),
                features=[
                    Feature(self.__last_path_to_uuid(feature_dir), feature_bytes) 
                    for (feature_bytes, feature_dir) in
                    await asyncio.gather(*
                        [
                            self.__read_feature(feature_filename_full_path) for feature_filename_full_path in [
                                    os.path.join(person_directory, feature_file_name) 
                                    for feature_file_name in os.listdir(person_directory)
                                    if self.__is_uuid(feature_file_name)
                            ]
                        ]
                    )
                ]
            )

    async def enumerate_features_idxs(self, persons_filter: Callable[[str], bool] = lambda f : True) -> Iterator[Tuple[uuid.UUID, uuid.UUID]]:
        if not os.path.exists(self.__directory):
            return
        
        for person_directory in map(self.__add_base_path_to_path, filter(persons_filter, filter(self.__is_uuid, os.listdir(self.__directory)))):
            yield (self.__last_path_to_uuid(person_directory), [uuid.UUID(directory) for directory in os.listdir(person_directory) if self.__is_uuid(directory)])


    async def __read_feature(self, feature_directory: str) -> Tuple[bytes, str]:
        async with aiofiles.open(file=feature_directory, mode='rb') as features_file:
            return (await features_file.read(), feature_directory)

    def __last_path_to_uuid(self, path : str) -> uuid.UUID:
        return uuid.UUID(os.path.split(path)[-1])

    def __add_base_path_to_path(self, *args : List[str]) -> str:
        return os.path.join(self.__directory, *args)

    def __is_uuid(self, name: str) -> bool:
        try:
            uuid.UUID(name)
            return True
        except:
            return False
        

    def __create_if_not_exists(self, directory) -> str:
        os.makedirs(directory, exist_ok=True)
        return directory


if __name__ == "__main__":
    async def main():
        path = 'D:/code/osu/osu-recognition/features'
        storage = FileFeaturesStorage(path)
        async for feature in storage.enumerate(lambda person_id : person_id == 'd5665071-16c6-4aae-be7c-09b9e96f0956'):
            print(feature)

    asyncio.get_event_loop().run_until_complete(main())