import aiofiles, uuid
from typing import List, Callable, Iterator
from aiofiles.base import AiofilesContextManager
import os
import asyncio
from abstractions.storages import PersonImages, ImagesStorage
from pathlib import Path


class FileImagesStorage(ImagesStorage):
    def __init__(self, directory : str):
        self.__directory : str = directory

    async def save(self, person_id: uuid.UUID, image_type: str, feature_id: uuid.UUID, image: bytes) -> None:
        person_directory = self.__create_if_not_exists(
            self.__add_base_path_to_path(str(person_id))
        )
        
        full_image_path = os.path.join(person_directory, f'{str(feature_id)}.{image_type}')

        async with aiofiles.open(file=full_image_path, mode='wb') as fp:
            await fp.write(image)


    async def enumerate(self, persons_filter: Callable[[str], bool] = lambda f : True) -> Iterator[PersonImages]:
        if not os.path.exists(self.__directory):
            return

        for person_directory in map(self.__add_base_path_to_path, filter(persons_filter, filter(self.__is_uuid, os.listdir(self.__directory)))):

            yield PersonImages(
                person_id=self.__last_path_to_uuid(person_directory),
                images_names=os.listdir(person_directory)
            )


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
        path = 'D:/code/osu/osu-recognition/images'
        storage = FileImagesStorage(path)
        async for feature in storage.enumerate():
            print(feature)

    asyncio.get_event_loop().run_until_complete(main())