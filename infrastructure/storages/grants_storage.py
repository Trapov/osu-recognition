import aiofiles, uuid
from typing import List, Callable
from aiofiles.base import AiofilesContextManager
import os
import asyncio


class PersonGrants():
    def __init__(self, person_id : uuid.UUID, grants: List[str]):
        self.grants : List[str] = grants
        self.person_id : uuid.UUID = person_id

    def __str__(self):
        return f'Person[{str(self.person_id)}] [{self.grants}] ]'

class GrantsStorage():
    def __init__(self, directory : str, grants_file_name: str = 'grants.txt'):
        self.__directory : str = directory
        self.__grants_file_name : str = grants_file_name

    async def enumerate(self, persons_filter: Callable[[str], bool] = lambda f : True) -> List[PersonGrants]:
        for person_directory in map(self.__format_path_from_base, filter(persons_filter, filter(self.__is_uuid, os.listdir(self.__directory)))):
            yield PersonGrants(
                person_id=self.__format_by_last_path_is_id(person_directory),
                grants=await self.__read_grants(self.__format_path_from_base(person_directory))
            )


    async def __read_grants(self, person_directory: str) -> List[str]:
        try:
            async with aiofiles.open(file=os.path.join(person_directory, self.__grants_file_name), mode='r+') as grants_file:
                return [line.strip() for line in await grants_file.readlines()]
        except:
            return []


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
        

if __name__ == "__main__":
    async def main():
        path = 'D:/code/osu/osu-recognition/features'
        storage = GrantsStorage(path)
        async for grant in storage.enumerate():
            print(grant)

    asyncio.get_event_loop().run_until_complete(main())