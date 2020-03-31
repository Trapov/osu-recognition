from infrastructure.container import ServicesContainer

import uuid

from abstractions import Page, User, UserFeatures, Feauture
from itertools import islice, groupby
from abstractions.storages import FeaturesStorage, ImagesStorage, GrantsStorage
import asyncio

async def __io_work_features(persons : dict, features_storage : FeaturesStorage):
    async for person_id, feature_id in features_storage.enumerate_features_idxs():
        persons.setdefault(person_id, {'person_id': person_id}).setdefault('features', []).append(feature_id)

async def __io_work_images(persons : dict, images_storage : ImagesStorage):
    async for person_images in images_storage.enumerate():
        persons.setdefault(person_images.person_id, {'person_id': person_images.person_id})['images_names'] = \
        [
            (uuid.UUID(image_name.split('.')[0]), image_name) for image_name in person_images.images_names
        ]

async def __io_work_grants(persons : dict, grants_storage: GrantsStorage):
    async for person_grants in grants_storage.enumerate():
        persons.setdefault(person_grants.person_id, {'person_id': person_grants.person_id})['grants'] = person_grants.grants

async def handle(offset: int, count: int, features_storage : FeaturesStorage, images_storage : ImagesStorage, grants_storage: GrantsStorage) -> Page[User]:

    persons = {}

    await asyncio.gather(
        __io_work_features(persons, features_storage),
        __io_work_images(persons, images_storage),
        __io_work_grants(persons, grants_storage)
    )

    users = [ 
        User(person['person_id'], 
            UserFeatures([
                Feauture(feature, image_name[1])
                for (feature, image_name) in zip(
                    sorted(person['features']),
                    sorted(person['images_names'], key=lambda img : img[0])
                )
            ]),
            person.get('grants', [])
        ) 
        for person in persons.values()
    ]

    total = len(users)
    values = list(islice(users, offset, offset + count))
    return Page(values, offset, total)