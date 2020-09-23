import aiofiles, uuid
from typing import List, Callable, AsyncIterator
from aiofiles.base import AiofilesContextManager
import os
import asyncio
from abstractions.storages import ImagesStorage
from pathlib import Path
import shutil, glob


class FileImagesStorage(ImagesStorage):
    def __init__(self, directory : str):
        self.__directory : str = directory

    async def delete_for_user(self, person_id: uuid.UUID, transaction_scope = None) -> None:
        self.__rm_r(self.__add_base_path_to_path(str(person_id)))

    async def delete(self, person_id: uuid.UUID, feature_id: uuid.UUID, transaction_scope = None):
        person_directory = self.__add_base_path_to_path(str(person_id))

        full_image_path = os.path.join(person_directory, f'{str(feature_id)}.*')
        found_files = glob.glob(full_image_path)
        if len(found_files) > 0:
            os.remove(found_files[0])


    async def get(self, person_id: uuid.UUID, feature_id: uuid.UUID):
        person_directory = self.__create_if_not_exists(
            self.__add_base_path_to_path(str(person_id))
        )
        
        full_image_path = os.path.join(person_directory, f'{str(feature_id)}.*')
        found_files = glob.glob(full_image_path)

        if len(found_files) == 0:
            raise FileNotFoundError(full_image_path)
        
        full_image_path = found_files[0]
        
        file_content = None
        async with aiofiles.open(file=full_image_path, mode='rb') as f:
            file_content = await f.read()

        return file_content


    async def save(self, person_id: uuid.UUID, image_type: str, feature_id: uuid.UUID, image: bytes, transaction_scope = None) -> None:
        person_directory = self.__create_if_not_exists(
            self.__add_base_path_to_path(str(person_id))
        )
        
        full_image_path = os.path.join(person_directory, f'{str(feature_id)}.{image_type}')

        async with aiofiles.open(file=full_image_path, mode='wb') as fp:
            await fp.write(image)


    def __rm_r(self, path):
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        elif os.path.exists(path):
            os.remove(path)

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
