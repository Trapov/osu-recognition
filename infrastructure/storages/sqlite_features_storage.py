import logging
import uuid
from typing import AsyncIterator

import aiosqlite

from abstractions.storages import FeaturesStorage
from abstractions import UserFeatures, Feature
from .sqlite_migrations import migration_scripts
import asyncio
from datetime import datetime


class SqliteFeaturesStorage(FeaturesStorage):
    def __init__(self, sqlite_file: str):
        self.__sqlite_file: str = sqlite_file
        self.__pooled_connection : aiosqlite.Connection = None
        
        asyncio.create_task(self.migrations()).add_done_callback(lambda _ : logging.info('Features migrations done'))

    async def save(self, user_id: uuid.UUID, feature_id: uuid.UUID, image_type: str, feature: bytes, created_at: datetime, transaction_scope = None) -> None:
        pooled_connection = transaction_scope if transaction_scope else self.__pooled_connection
        
        if not pooled_connection:
            pooled_connection = self.__pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            pooled_connection.row_factory = aiosqlite.Row

        await pooled_connection.execute('insert or replace into "Feature" ("user_id", "feature_id", "image_type", "feature", "created_at") values(?, ?, ?, ?, ?)',
            parameters=[str(user_id), str(feature_id), image_type, feature, str(created_at)])
        
        if not transaction_scope:
            await pooled_connection.commit()

    async def delete(self, user_id: uuid.UUID, idx: uuid.UUID, transaction_scope = None):
        pooled_connection = transaction_scope if transaction_scope else self.__pooled_connection

        if not pooled_connection:
            pooled_connection = self.__pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            pooled_connection.row_factory = aiosqlite.Row

        await pooled_connection.execute('''
            PRAGMA foreign_keys = ON;
        ''')
        await pooled_connection.execute('''
            delete from "Feature"  
            where "user_id"=? and "feature_id"= ?
        ''', parameters=[str(user_id), str(idx)]
        )

        if not transaction_scope:
            await pooled_connection.commit()


    async def enumerate_for(self, idx : uuid.UUID) -> AsyncIterator[UserFeatures]:
        if not self.__pooled_connection:
            self.__pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            self.__pooled_connection.row_factory = aiosqlite.Row

        async with self.__pooled_connection.execute('''
                select 
                    "user_id",
                    "feature_id",
                    "image_type",
                    "feature",
                    "created_at"
                from "Feature"
                where "user_id" = ?
            ''', [str(idx)]) as cursor:
            current_user_features: UserFeatures = None
            async for row in cursor:

                row_user_id = uuid.UUID(row[0])
                row_feature_id = uuid.UUID(row[1])

                if not current_user_features:
                    current_user_features = UserFeatures(row_user_id, [])
                elif current_user_features.user_id != row_user_id:
                    yield current_user_features
                    current_user_features = UserFeatures(row_user_id, [])

                current_user_features.features.append(
                    Feature(idx=row_feature_id, image_type=row[2], feature=row[3], created_at=datetime.fromisoformat(row[4])))
                
            if current_user_features:
                yield current_user_features
            else:
                return

    async def enumerate(self) -> AsyncIterator[UserFeatures]:
        if not self.__pooled_connection:
            self.__pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            self.__pooled_connection.row_factory = aiosqlite.Row

        async with self.__pooled_connection.execute('''
                select 
                    "user_id",
                    "feature_id",
                    "image_type",
                    "feature",
                    "created_at"
                from "Feature"
                order by "user_id"
            ''') as cursor:
            current_user_features: UserFeatures = None
            async for row in cursor:

                row_user_id = uuid.UUID(row[0])
                row_feature_id = uuid.UUID(row[1])

                if not current_user_features:
                    current_user_features = UserFeatures(row_user_id, [])
                elif current_user_features.user_id != row_user_id:
                    yield current_user_features
                    current_user_features = UserFeatures(row_user_id, [])

                current_user_features.features.append(
                    Feature(idx=row_feature_id, image_type=row[2], feature=row[3], created_at=datetime.fromisoformat(row[4])))
                
            if current_user_features:
                yield current_user_features
            else:
                return

    async def migrations(self) -> None:
        async with aiosqlite.connect(self.__sqlite_file) as db:

            for migration_script in migration_scripts:
                await db.execute(migration_script)
            
            await db.commit()
