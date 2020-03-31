import aiofiles, uuid
from typing import List, Callable, Iterator
from aiofiles.base import AiofilesContextManager
import os
import asyncio
from abstractions.storages import PersonGrants, GrantsStorage


class FileGrantsStorage(GrantsStorage):
    def __init__(self, directory : str, grants_file_name: str = 'grants.txt'):
        self.__directory : str = directory
        self.__grants_file_name : str = grants_file_name

    async def enumerate(self, persons_filter: Callable[[str], bool] = lambda f : True) -> Iterator[PersonGrants]:
        if not os.path.exists(self.__directory):
            return

        for person_directory in map(self.__add_base_path_to_path, filter(persons_filter, filter(self.__is_uuid, os.listdir(self.__directory)))):
            yield PersonGrants(
                person_id=self.__last_path_to_uuid(person_directory),
                grants=await self.__read_grants(person_directory)
            )


    async def __read_grants(self, person_directory: str) -> Iterator[str]:
        try:
            async with aiofiles.open(file=os.path.join(person_directory, self.__grants_file_name), mode='r') as grants_file:
                return (line.strip() for line in await grants_file.readlines())
        except:
            return []


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
        

if __name__ == "__main__":
    async def main():
        path = 'D:/code/osu/osu-recognition/features'
        storage = FileGrantsStorage(path)
        async for grant in storage.enumerate():
            print(grant)

    asyncio.get_event_loop().run_until_complete(main())