from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
import uuid, logging.config
from uuid import UUID
from typing import List
from pydantic import BaseModel
from abstractions import User
from infrastructure.container import SINGLETON_CONTAINER
from infrastructure.images import get_ndarray_image

from use_cases import create_or_get_user, get_paged_users, to_token_grants, add_grants_for_user, remove_grants_for_user

app = FastAPI(title='REST-API. Recognition-Auth', version="1.0.0")
app.mount('/users', StaticFiles(directory="./images", check_dir=False), 'person_faces')

app.mount('/client', StaticFiles(directory='./ui/client', check_dir=True, html=True), 'ui_client')
app.mount('/admin', StaticFiles(directory='./ui/admin', check_dir=True, html=True), 'ui_admin')

from .logging_configuration import LOGGING
logging.config.dictConfig(LOGGING)

import mimetypes
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')

class GrantsBinding(BaseModel):
    user_id: UUID
    grant: str

class TokenIssue(BaseModel):
    user_id: UUID

@app.post("/tokens", tags=['tokens'], status_code=201)
async def users_tokens_get(*, token_issue: TokenIssue) -> dict:
    try:
        return {
            'token' : await to_token_grants.handle(token_issue.user_id, SINGLETON_CONTAINER.users_storage, SINGLETON_CONTAINER.grants_crypto)
        }
    except to_token_grants.NoGrantsFound:
        raise HTTPException(status_code=422, detail='No grants found. Nothing to authorize. Create them first for the user your issued the token.')

@app.post("/grants", tags=['grants'], status_code=201)
async def grants_post(*, grant: GrantsBinding) -> dict:
    try:
        await add_grants_for_user.handle(grant.user_id, grant.grant, SINGLETON_CONTAINER.users_storage)
        return Response(status_code=201)
    except add_grants_for_user.UserNotFound:
        raise HTTPException(status_code=404, detail='No user found. Create user first.')

@app.delete("/grants", tags=['grants'], status_code=201)
async def grants_delete(*, grant: GrantsBinding) -> dict:
    try:
        await remove_grants_for_user.handle(grant.user_id, grant.grant, SINGLETON_CONTAINER.users_storage)
        return Response(status_code=201)
    except add_grants_for_user.UserNotFound:
        raise HTTPException(status_code=404, detail='No user found. Create user first.')

@app.post("/users", tags=['users'], status_code=201)
async def login_post(*, file: UploadFile  = File(...)):
    img_bytes = await file.read()
    file_ext = file.filename.split('.')[-1]

    try:
        user_id = await create_or_get_user.handle(create_or_get_user.InputImage(img_bytes, file_ext),
            SINGLETON_CONTAINER.detector, 
            SINGLETON_CONTAINER.extractor,
            SINGLETON_CONTAINER.features_storage,
            SINGLETON_CONTAINER.distance_estimator,
            SINGLETON_CONTAINER.users_storage,
            SINGLETON_CONTAINER.images_storage)
        return {
            'id': user_id
        }

    except create_or_get_user.NoFacesFound:
        raise HTTPException(status_code=400, detail='No faces found. Try uploading another image.')
    except create_or_get_user.NoFeaturesExtracted:
        raise HTTPException(status_code=400, detail='Faces found, but no features extracted from the face, Try contacting the support.')

@app.get("/users", tags=['users'], status_code=200)
async def users_get(*, offset: int = Query(0), count: int = Query(20)) -> List[User]:
    users = await get_paged_users.handle(offset, count, SINGLETON_CONTAINER.users_storage)
    return {
        'offset': offset,
        'count': count,
        'total': users.total,
        'values': [ 
            { 
                'id': u.idx,
                'features': {
                    'count': u.features.count,
                    'values': [
                        { 
                            'feature_id' : feature.idx,
                            'image_name' : feature.image_name,
                            'created_at': feature.created_at
                        } 
                        for feature in u.features.features
                    ]
                },
                'grants': u.grants,
                'created_at': u.created_at
            } for u in users.values 
        ]
    }