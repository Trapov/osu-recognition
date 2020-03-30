from infrastructure.container import ServicesContainer
## todo: remove infrastructure, allow calling side to supply dependencies

from abstractions import Page, User
from itertools import islice

async def handle(offset : int, count : int, container : ServicesContainer) -> Page[User]:
    result = list([page async for page in container.storage.paged_users()])
    total = len(result)

    values = list(islice(result, offset, offset + count))

    return Page(values, offset, total)