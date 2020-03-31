from abstractions import GrantsCrypto
from abstractions.storages import GrantsStorage
from uuid import UUID

async def handle(user_id : UUID, grants_storage : GrantsStorage, grants_crypto: GrantsCrypto) -> str:
    grants = next(iter([grant async for grant in grants_storage.enumerate(lambda person: person == str(user_id))]), None)
    
    if not grants or grants.grants:
        raise Exception("No grants found. Nothing to authorize.")
    
    return grants_crypto.to_token(user_id, grants)
    