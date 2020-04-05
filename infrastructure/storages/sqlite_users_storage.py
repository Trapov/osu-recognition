import asyncio
import logging
import uuid
from typing import AsyncIterator

import aiosqlite

from abstractions import User, UserFeatures, Feature
from abstractions.storages import UsersStorage
from .sqlite_migrations import migration_scripts
import datetime


class SqliteUsersStorage(UsersStorage):
    def __init__(self, sqlite_file: str):
        self.__sqlite_file: str = sqlite_file        
        self.__read_pooled_connection : aiosqlite.Connection = None

        asyncio.create_task(self.migrations()).add_done_callback(lambda _ : logging.info('Users migrations done'))

    async def upsert(self, user_id: uuid.UUID, created_at: datetime.datetime) -> None:
        async with aiosqlite.connect(self.__sqlite_file) as db:
            await db.execute('''
                insert or ignore into "User" ("user_id", "created_at") values(?,?)
            ''', parameters=[str(user_id), str(created_at)]
            )
            await db.commit()

    async def count(self) -> int:
        if not self.__read_pooled_connection:
            self.__read_pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            self.__read_pooled_connection.row_factory = aiosqlite.Row

        async with self.__read_pooled_connection.execute('''
            select count(1)
            from "User" p
            join "Feature" f on f."user_id" = p."user_id"
            left join "Grant" g on g."user_id" = p."user_id"
        ''') as cursor:
            return (await cursor.fetchone())[0]

    async def single_no_features(self, user_id: uuid.UUID):
        user = None

        if not self.__read_pooled_connection:
            self.__read_pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            self.__read_pooled_connection.row_factory = aiosqlite.Row

        async with self.__read_pooled_connection.execute('''
            select 
                p."user_id",
                f."feature_id",
                f."image_type",
                f."created_at" as "feature_created_at",
                g."grant",
                g."created_at" as "grant_created_at",
                p."created_at" as "user_created_at"
            from "User" p
            join "Feature" f on f."user_id" = p."user_id"
            where p."user_id" = ?
            left join "Grant" g on g."user_id" = p."user_id"
            order by p."user_id", p."created_at"
        ''', parameters=[str(user_id)]) as cursor:
            async for row in cursor:
                if not user:
                    user = User(idx=user_id, user_features=UserFeatures(user_id, features=[]), grants=[], created_at=datetime.datetime.fromisoformat(row['user_created_at']))

                if row['grant']:
                    user.grants.append(row['grant'])

                user.features.features.append(
                    Feature(
                        uuid.UUID(row['feature_id']),
                        row['image_type'], 
                        datetime.datetime.fromisoformat(row['feature_created_at']), 
                        []
                    )
                )

        return user

    async def enumerate(self, offset: int = None, limit: int = None) -> AsyncIterator[User]:
        if not self.__read_pooled_connection:
            self.__read_pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            self.__read_pooled_connection.row_factory = aiosqlite.Row

        async with self.__read_pooled_connection.execute('''
            select 
                p."user_id",
                f."feature_id",
                f."image_type",
                f."created_at" as "feature_created_at",
                g."grant",
                g."created_at" as "grant_created_at",
                p."created_at" as "user_created_at"
            from "User" p
            join "Feature" f on f."user_id" = p."user_id"
            left join "Grant" g on g."user_id" = p."user_id"
            order by p."user_id", p."created_at"
            limit ? offset ?
        ''', parameters=[limit, offset]) as cursor:
            current_user_features: User = None
            async for row in cursor:
                row_user_id = uuid.UUID(row['user_id'])

                if not current_user_features:
                    current_user_features = User(row_user_id, UserFeatures(row_user_id, []), grants=[], created_at=datetime.datetime.fromisoformat(row['user_created_at']))
                if current_user_features.idx != row_user_id:
                    yield current_user_features
                    current_user_features = User(row_user_id, UserFeatures(row_user_id, []), grants=[], created_at=datetime.datetime.fromisoformat(row['user_created_at']))

                if row['grant']:
                    current_user_features.grants.append(
                        row['grant']   
                    )

                current_user_features.features.features.append(
                    Feature(
                        uuid.UUID(row['feature_id']),
                        row['image_type'],
                        datetime.datetime.fromisoformat(row['feature_created_at']), []
                    )
                )

            if current_user_features:
                yield current_user_features
            else:
                return

    async def migrations(self) -> None:
        async with aiosqlite.connect(self.__sqlite_file) as db:
            
            for migration_script in migration_scripts:
                await db.execute(migration_script)
            
            await db.commit()
