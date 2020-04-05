from abstractions import Page, User
from abstractions.storages import UsersStorage


async def handle(
        offset: int,
        count: int,
        users_storage: UsersStorage) -> Page[User]:
    total = await users_storage.count()

    if total == 0:
        return Page(values=[], offset=offset, total=total)

    values = [value async for value in users_storage.enumerate(offset=offset, limit=count)]

    return Page(values, offset, total)
