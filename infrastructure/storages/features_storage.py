import aiofiles, uuid
from typing import List, Tuple, Callable
from aiofiles.base import AiofilesContextManager
import os
import asyncio

class Feature():
    def __init__(self, feature_id : uuid.UUID, feature: bytes):
        self.feature_id : uuid.UUID = feature_id
        self.feature : bytes = feature

    def __str__(self):
        return f'Feature[{str(self.feature_id)}] [{len(self.feature)}] bytes.'

class PersonFeatures():
    def __init__(self, person_id : uuid.UUID, features: List[Feature]):
        self.features : List[Feature] = features
        self.person_id : uuid.UUID = person_id

    def __str__(self):
        return f'Person[{str(self.person_id)}] [ {[str(feature) for feature in self.features]} ]'

class FeaturesStorage():
    def __init__(self, directory : str):
        self.__directory : str = directory

    async def save(self, person_id: uuid.UUID, feature_id: uuid.UUID, feature: bytes) -> None:
        directory_to_save = self.__create_if_not_exists(
                self.__format_path_to_feature(
                    person_id=person_id,
                    feature_id=feature_id
            )
        )

        async with aiofiles.open(file=directory_to_save, mode='wb+') as fp:
            await fp.write(feature)


    async def enumerate(self, persons_filter: Callable[[str], bool] = lambda f : True) -> List[PersonFeatures]:
        for person_directory in map(self.__format_path_from_base, filter(persons_filter, filter(self.__is_uuid, os.listdir(self.__directory)))):
            yield PersonFeatures(
                person_id=self.__format_by_last_path_is_id(person_directory),
                features=[
                    Feature(self.__format_by_last_path_is_id(feature_dir), feature_bytes) 
                    for (feature_bytes, feature_dir) in
                    await asyncio.gather(*
                        [
                            self.__read_feature(feature_filename_full_path) for feature_filename_full_path in [
                                    self.__format_path_from_base(person_directory, feature_file_name) 
                                    for feature_file_name in os.listdir(person_directory)
                                    if self.__is_uuid(feature_file_name)
                            ]
                        ]
                    )
                ]
            )


    async def __read_feature(self, feature_directory: str) -> Tuple[bytes, str]:
        async with aiofiles.open(file=feature_directory, mode='rb+') as features_file:
            return (await features_file.read(), feature_directory)

    def __format_path_to_feature(self, person_id : uuid.UUID, feature_id: uuid.UUID) -> str:
        return os.path.join(self.__directory, person_id, feature_id)

    def __format_by_last_path_is_id(self, path : str) -> uuid.UUID:
        return uuid.UUID(os.path.split(path)[-1])

    def __format_path_from_base(self, *args : List[str]) -> str:
        return os.path.join(self.__directory, *args)

    def __is_uuid(self, name: str) -> bool:
        try:
            uuid.UUID(name)
            return True
        except:
            return False
        

    @staticmethod
    def __create_if_not_exists(self, directory) -> str:
        if not os.path.exists(directory):
            os.mkdir(directory)
        
        return directory


if __name__ == "__main__":
    async def main():
        path = 'D:/code/osu/osu-recognition/features'
        storage = FeaturesStorage(path)
        async for feature in storage.enumerate(lambda person_id : person_id == 'd5665071-16c6-4aae-be7c-09b9e96f0956'):
            print(feature)

    asyncio.get_event_loop().run_until_complete(main())