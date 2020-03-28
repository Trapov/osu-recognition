from fastapi import FastAPI, File, UploadFile, Query
import uuid
from typing import List

from infrastructure.storages import FileStorage, User
from infrastructure.container import SINGLETON_CONTAINER
from infrastructure.images import get_ndarray_image

from use_cases import create_or_get_user, get_paged_users

app = FastAPI()

@app.post("/users")
async def login_post(*, file: UploadFile  = File(...)):
    img_bytes = await file.read()

    user = create_or_get_user.handle(img_bytes, SINGLETON_CONTAINER)

    return {
        'id': user.idx,
        'features_count': user.features_count,
        'grants': user.grants
    }

@app.get("/users")
async def users_get(*, offset: int = Query(0), count: int = Query(20)) -> List[User]:
    users = get_paged_users.handle(offset, count, SINGLETON_CONTAINER)
    return {
        'offset': offset,
        'count': count,
        'total': users.total,
        'values': [ 
            { 
                'id': u.idx,
                'features_count': u.features_count,
                'grants': u.grants 
            } for u in users.values ]
    }