from infrastructure.container import ServicesContainer
## todo: remove infrastructure, allow calling side to supply dependencies
from uuid import UUID

async def handle(user_id : UUID, container : ServicesContainer) -> str:
    grants = await container.storage.get_grants(user_id)
    
    if len(grants) > 0:
        return container.grants_crypto.to_token(user_id, grants)
    
    raise Exception("No grants found. Nothing to authorize.")