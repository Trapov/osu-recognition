from abstractions import GrantsCrypto
from abstractions.storages import GrantsStorage
from uuid import UUID

class NoGrantsFound(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

async def handle(user_id : UUID, grants_storage : GrantsStorage, grants_crypto: GrantsCrypto) -> str:
    grants = next(iter([grant async for grant in grants_storage.enumerate(lambda person: person == str(user_id))]), None)
    
    if not grants or not grants.grants:
        raise NoGrantsFound()
    
    return grants_crypto.to_token(user_id, list(grants.grants))
    