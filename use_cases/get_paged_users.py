from infrastructure.container import ServicesContainer
from abstractions import Page, User
from itertools import islice

def handle(offset : int, count : int, container : ServicesContainer) -> Page[User]:
    result = list(container.storage.paged_users())
    total = len(result)

    values = list(islice(result, offset, offset + count))

    return Page(values, offset, total)