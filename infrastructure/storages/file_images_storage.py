import aiofiles, uuid
from typing import List, Callable, AsyncIterator
from aiofiles.base import AiofilesContextManager
import os
import asyncio
from abstractions.storages import ImagesStorage
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
