from fastapi import FastAPI, File, UploadFile, Query, Path, HTTPException, Depends
from fastapi.security import HTTPBearer
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from os import environ, getpid
import uuid, logging.config
from uuid import UUID
from typing import List
from pydantic import BaseModel
from abstractions import User
from infrastructure.container import SINGLETON_CONTAINER

from psutil import Process, virtual_memory

from infrastructure.images import get_ndarray_image

from use_cases import \
    create_or_get_user, \
    get_paged_users, \
    to_token_grants, \
    add_grants_for_user,\
    remove_grants_for_user, \
    get_single_user_from_token, \
    get_paged_recognition_settings, \
    save_or_update_recognition_settings, \
    get_current_recognition_settings, \
    create_or_get_distances_for, \
    delete_user, \
    delete_feature, \
    link_user, \
    link_feature

bearer = HTTPBearer()

app = FastAPI(title='REST-API. Recognition-Auth', version="1.0.0")


app.mount('/client', StaticFiles(directory='./ui/client', check_dir=True, html=True), 'ui_client')
app.mount('/admin', StaticFiles(directory='./ui/admin', check_dir=True, html=True), 'ui_admin')

from .logging_configuration import LOGGING, configure
get_top_logs = configure(LOGGING)

import mimetypes
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')

class GrantsBinding(BaseModel):
    user_id: UUID
    grant: str

class ResizeFactors(BaseModel):
    x : float
    y : float

class LinkUserFeature(BaseModel):
    user_id: UUID
    user_id_to: UUID
    feature_id: UUID

class LinkUser(BaseModel):
    user_id: UUID
    user_id_to: UUID

class RecognitionSettingsBinding(BaseModel):
    name: str
    is_active: bool
    max_features: int
    base_threshold: float
    rate_of_decreasing_threshold_with_each_feature: float
    resize_factors: ResizeFactors

class TokenIssue(BaseModel):
    user_id: UUID

ADMIN_TOKEN = environ.get('ADMIN_TOKEN', 'HACK')

def raise_if_not_admin(credentials : str) -> None:
    if credentials != ADMIN_TOKEN:
        raise HTTPException(401, 'Not authorized')

@app.get("/logs", tags=['logs'], status_code=200)
async def logs_get(*, token: HTTPBearer = Depends(bearer)) -> dict:
    raise_if_not_admin(token.credentials)
    return get_top_logs()
    
@app.get("/metrics", tags=['metrics'], status_code=200)
async def metrics_get(*, token: HTTPBearer = Depends(bearer)) -> dict:
    raise_if_not_admin(token.credentials)
    prc = Process(getpid())
    return {
        "memory": {
            'used': prc.memory_info().vms,
            'total': virtual_memory().total
        },
        "cpu": {
            "utilization" : prc.cpu_percent()
        }
    }

@app.post("/tokens", tags=['tokens'], status_code=201)
async def users_tokens_get(*, token: HTTPBearer = Depends(bearer), token_issue: TokenIssue) -> dict:
    try:
        raise_if_not_admin(token.credentials)

        return {
            'token' : await to_token_grants.handle(token_issue.user_id, SINGLETON_CONTAINER.users_storage, SINGLETON_CONTAINER.grants_crypto)
        }
    except to_token_grants.NoGrantsFound:
        raise HTTPException(status_code=422, detail='No grants found. Nothing to authorize. Create them first for the user your issued the token.')

@app.post("/grants", tags=['grants'], status_code=201)
async def grants_post(*, token: HTTPBearer = Depends(bearer), grant: GrantsBinding) -> dict:
    try:
        raise_if_not_admin(token.credentials)

        await add_grants_for_user.handle(grant.user_id, grant.grant, SINGLETON_CONTAINER.users_storage)
        return Response(status_code=201)
    except add_grants_for_user.UserNotFound:
        raise HTTPException(status_code=404, detail='No user found. Create user first.')

@app.delete("/grants", tags=['grants'], status_code=201)
async def grants_delete(*, token: HTTPBearer = Depends(bearer), grant: GrantsBinding) -> dict:
    try:
        raise_if_not_admin(token.credentials)

        await remove_grants_for_user.handle(grant.user_id, grant.grant, SINGLETON_CONTAINER.users_storage)
        return Response(status_code=201)
    except add_grants_for_user.UserNotFound:
        raise HTTPException(status_code=404, detail='No user found. Create user first.')

@app.get("/users/{idx}/nearest", tags=['users'], status_code=200)
async def get_nearest(*, idx : uuid.UUID, token: HTTPBearer = Depends(bearer)):
    raise_if_not_admin(token.credentials)
    result = await create_or_get_distances_for.handle(
            idx,
            SINGLETON_CONTAINER.features_storage,
            SINGLETON_CONTAINER.distance_estimator,
            SINGLETON_CONTAINER.users_storage
        )
    
    return result

@app.patch("/users/link/feature", tags=['users'], status_code=200)
async def path_link_user_feature(*, token: HTTPBearer = Depends(bearer), link_binding: LinkUserFeature):
    raise_if_not_admin(token.credentials)

    await link_feature.handle(
        link_binding.user_id,
        link_binding.feature_id,
        link_binding.user_id_to,
        SINGLETON_CONTAINER.images_storage,
        SINGLETON_CONTAINER.users_storage,
        SINGLETON_CONTAINER.features_storage
    )

    return Response(status_code=200)

@app.patch("/users/link", tags=["users"], status_code=200)
async def patch_link_user(*, token: HTTPBearer = Depends(bearer), link_binding: LinkUser):
    raise_if_not_admin(token.credentials)

    await link_user.handle(
        link_binding.user_id,
        link_binding.user_id_to,
        SINGLETON_CONTAINER.images_storage,
        SINGLETON_CONTAINER.users_storage,
        SINGLETON_CONTAINER.features_storage
    )

    return Response(status_code=200)

@app.delete("/users/{idx}", tags=['users'], status_code=200)
async def delete_iser(*, idx: uuid.UUID, token: HTTPBearer = Depends(bearer)):
    raise_if_not_admin(token.credentials)

    await delete_user.handle(
        user_id=idx,
        images_storage=SINGLETON_CONTAINER.images_storage,
        users_storage=SINGLETON_CONTAINER.users_storage
    )
    
    return Response(status_code=200)
    
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
            SINGLETON_CONTAINER.recognition_settings_storage,
            SINGLETON_CONTAINER.images_storage)

        token = await to_token_grants.handle(user_id, SINGLETON_CONTAINER.users_storage, SINGLETON_CONTAINER.grants_crypto)
        
        return {
            'token': token
        }

    except create_or_get_user.NoFacesFound:
        raise HTTPException(status_code=400, detail='No faces found. Try uploading another image.')
    except create_or_get_user.NoFeaturesExtracted:
        raise HTTPException(status_code=400, detail='Faces found, but no features extracted from the face, Try contacting the support.')

@app.delete("/users/{user_id}/features/{feature_id}", tags=['users'], status_code=200)
async def feature_delete(*, user_id: uuid.UUID, feature_id: uuid.UUID, token: HTTPBearer = Depends(bearer)):
    raise_if_not_admin(token.credentials)

    await delete_feature.handle(
        user_id=user_id,
        feature_id=feature_id,
        images_storage=SINGLETON_CONTAINER.images_storage,
        features_storage=SINGLETON_CONTAINER.features_storage
    )

    return Response(status_code=200)


@app.post("/settings", tags=['settings'], status_code=201)
async def settings_save(*, token: HTTPBearer = Depends(bearer), settings : RecognitionSettingsBinding) -> None:
    raise_if_not_admin(token.credentials)
    await save_or_update_recognition_settings.handle(
        name=settings.name, is_active=settings.is_active, max_features=settings.max_features,
        base_threshold=settings.base_threshold, rate_of_decreasing_threshold_with_each_feature=settings.rate_of_decreasing_threshold_with_each_feature,
        resize_factors_x=settings.resize_factors.x, resize_factors_y=settings.resize_factors.y, settings_storage=SINGLETON_CONTAINER.recognition_settings_storage
    )
    return Response(status_code=201)

@app.get("/settings/current", tags=['settings'], status_code=200)
async def settings_get(*, token: HTTPBearer = Depends(bearer)) -> dict:

    raise_if_not_admin(token.credentials)

    result = await get_current_recognition_settings.handle(settings_storage=SINGLETON_CONTAINER.recognition_settings_storage)
    return {
        'name': result.name,
        "name" : result.name,
        "is_active" : result.is_active,
        "max_features" : result.max_features,
        "base_threshold" : result.base_threshold,
        "rate_of_decreasing_threshold_with_each_feature" : result.rate_of_decreasing_threshold_with_each_feature,
        "created_at" : result.created_at,
        "updated_at" : result.updated_at,
        "resize_factors" : {
            'x': result.resize_factors.x,
            'y': result.resize_factors.y
        }
    }


@app.get("/settings", tags=['settings'], status_code=200)
async def settings_get(*, token: HTTPBearer = Depends(bearer), offset: int = Query(0), count: int = Query(20)) -> List[dict]:

    raise_if_not_admin(token.credentials)

    result = await get_paged_recognition_settings.handle(offset=offset, count=count, settings_storage=SINGLETON_CONTAINER.recognition_settings_storage)
    return {
        'offset': offset,
        'count': count,
        'total': result.total,
        'values': [ 
            { 
                'name': rs.name,
                "name" : rs.name,
                "is_active" : rs.is_active,
                "max_features" : rs.max_features,
                "base_threshold" : rs.base_threshold,
                "rate_of_decreasing_threshold_with_each_feature" : rs.rate_of_decreasing_threshold_with_each_feature,
                "created_at" : rs.created_at,
                "updated_at" : rs.updated_at,
                "resize_factors" : {
                    'x': rs.resize_factors.x,
                    'y': rs.resize_factors.y
                }
            } for rs in result.values
        ]
    }


@app.get("/users", tags=['users'], status_code=200)
async def users_get(*, token: HTTPBearer = Depends(bearer), offset: int = Query(0), count: int = Query(20)) -> List[User]:

    raise_if_not_admin(token.credentials)

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

@app.get("/me", tags=['user'], status_code=200)
async def user_get_me(*, token: HTTPBearer = Depends(bearer)) -> User:
    user = await get_single_user_from_token.handle(token=token.credentials, users_storage=SINGLETON_CONTAINER.users_storage, grants_crypto=SINGLETON_CONTAINER.grants_crypto)
    
    if not user:
        raise HTTPException(401, 'Not authorized')
    
    return {
        'id': user.idx,
        'features': {
            'count': user.features.count,
            'values': [
                { 
                    'feature_id' : feature.idx,
                    'image_name' : feature.image_name,
                    'created_at': feature.created_at
                }
                for feature in user.features.features
            ]
        },
        'grants': user.grants,
        'created_at': user.created_at
    }

app.mount('/users', StaticFiles(directory="./images", check_dir=False), 'person_faces')
app.mount('/', StaticFiles(directory='./ui', check_dir=True, html=True), 'ui_entry')