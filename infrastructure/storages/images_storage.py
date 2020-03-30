import aiofiles, uuid
from typing import List, Callable
from aiofiles.base import AiofilesContextManager
import os
import asyncio

class PersonImages():
    def __init__(self, person_id : uuid.UUID, images_names : List[str]):
        self.images_names : List[str] = images_names
        self.person_id : uuid.UUID = person_id

    def __str__(self):
        return f'Person[{str(self.person_id)}] [ {self.images_names} ]'

class ImagesStorage():
    def __init__(self, directory : str):
        self.__directory : str = directory

    async def save(self, person_id: uuid.UUID, image_type: str, feature_id: uuid.UUID, image: bytes) -> None:
        directory_to_save = self.__create_if_not_exists(
                self.__format_path_to_image(
                    person_id=person_id,
                    feature_id=feature_id,
                    type=image_type
            )
        )

        async with aiofiles.open(file=directory_to_save, mode='wb+') as fp:
            await fp.write(image)


    async def enumerate(self, persons_filter: Callable[[str], bool] = lambda f : True) -> List[PersonImages]:
        for person_directory in map(self.__format_path_from_base, filter(persons_filter, filter(self.__is_uuid, os.listdir(self.__directory)))):

            yield PersonImages(
                person_id=self.__format_by_last_path_is_id(person_directory),
                images_names=os.listdir(person_directory)
            )


    def __format_path_to_image(self, person_id : uuid.UUID, feature_id: uuid.UUID) -> str:
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
        path = 'D:/code/osu/osu-recognition/images'
        storage = ImagesStorage(path)
        async for feature in storage.enumerate():
            print(feature)

    asyncio.get_event_loop().run_until_complete(main())