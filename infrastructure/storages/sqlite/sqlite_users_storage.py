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

        self.__pooled_connection : aiosqlite.Connection = None
        asyncio.create_task(self.migrations()).add_done_callback(lambda _ : logging.info('Users migrations done'))

    async def upsert(self, user_id: uuid.UUID, created_at: datetime.datetime, transaction_scope = None) -> None:
        pooled_connection = transaction_scope if transaction_scope else self.__pooled_connection

        if not pooled_connection:
            pooled_connection = self.__pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            pooled_connection.row_factory = aiosqlite.Row

        await pooled_connection.execute('''
            insert or replace into "User" ("user_id", "created_at") values(?,?)
        ''', parameters=[str(user_id), str(created_at)]
        )

        if not transaction_scope:
            await self.__pooled_connection.commit()


    async def delete_user(self, user_id, transaction_scope = None) -> None:
        pooled_connection = transaction_scope if transaction_scope else self.__pooled_connection

        if not pooled_connection:
            pooled_connection = self.__pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            pooled_connection.row_factory = aiosqlite.Row

        await pooled_connection.execute('''
            PRAGMA foreign_keys = ON;
        ''')

        await pooled_connection.execute('''
            delete from "User"  
            where "user_id"= ?
        ''', parameters=[str(user_id)]
        )

        if not transaction_scope:
            await pooled_connection.commit()

    async def delete_grant(self, user_id: uuid.UUID, grant: str, transaction_scope = None) -> None:
        pooled_connection = transaction_scope if transaction_scope else self.__pooled_connection

        if not pooled_connection:
            pooled_connection = self.__pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            pooled_connection.row_factory = aiosqlite.Row

        await pooled_connection.execute('''
            PRAGMA foreign_keys = ON;
        ''')
        
        await pooled_connection.execute('''
            delete from "Grant"  
            where "user_id"= ? and "grant" = ?
        ''', parameters=[str(user_id), str(grant)]
        )

        if not transaction_scope:
            await pooled_connection.commit()


    async def save(self, user: User, transaction_scope = None) -> None:
        pooled_connection = await self.get_pooled_connection_or_transaction_connection(transaction_scope)

        await pooled_connection.execute('''
            insert or ignore into "User" ("user_id", "created_at") values(?,?)
        ''', parameters=[str(user.idx), str(user.created_at)]
        )

        features = [(str(user.idx), str(f.idx), str(f.idx), f.feature, str(f.created_at)) for f in user.features.features]
        grants = [(str(user.idx), g, str(datetime.datetime.utcnow())) for g in user.grants]

        if len(features) > 0:
            for f in features:
                await pooled_connection.execute('''
                    insert or ignore into "Feature" ("user_id", "feature_id", "image_id", "feature", "created_at") values(?, ?, ?, ?, ?)
                ''', f)

        if len(grants) > 0:
            for g in grants:
                await pooled_connection.execute('''
                    insert or ignore into "Grant" ("user_id", "grant", "created_at") values(?, ?, ?)
                ''', g)

        if not transaction_scope:
            await pooled_connection.commit()


    async def count(self) -> int:
        if not self.__pooled_connection:
            self.__pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            self.__pooled_connection.row_factory = aiosqlite.Row

        async with self.__pooled_connection.execute('''
            select count(distinct p."user_id")
            from "User" p
            join "Feature" f on f."user_id" = p."user_id"
            left join "Grant" g on g."user_id" = p."user_id"
        ''') as cursor:
            return (await cursor.fetchone())[0]

    async def single_no_features(self, user_id: uuid.UUID) -> User:
        user = None

        pooled_connection = await self.get_pooled_connection_or_transaction_connection()

        async with pooled_connection.execute('''
            select 
                p."user_id",
                f."feature_id",
                i."image_type",
                f."created_at" as "feature_created_at",
                g."grant",
                g."created_at" as "grant_created_at",
                p."created_at" as "user_created_at"
            from "User" p
            join "Feature" f on f."user_id" = p."user_id"
            join "Image" i on i."image_id" = f."image_id"
            left outer join "Grant" g on g."user_id" = p."user_id"
            where p."user_id" = ?
            order by p."user_id", p."created_at"
        ''', parameters=[str(user_id)]) as cursor:
            async for row in cursor:
                if not user:
                    user = User(idx=user_id, user_features=UserFeatures(user_id, features=[]), grants=[], created_at=datetime.datetime.fromisoformat(row['user_created_at']))

                if row['grant'] and not(row['grant'] in user.grants):
                    user.grants.append(row['grant'])

                user.features.features.append(
                    Feature(
                        uuid.UUID(row['feature_id']),
                        row['image_type'], 
                        datetime.datetime.fromisoformat(row['feature_created_at']), 
                        b''
                    )
                )

        return user

    async def enumerate(self, offset: int = None, limit: int = None) -> AsyncIterator[User]:
        pooled_connection = await self.get_pooled_connection_or_transaction_connection()

        async with pooled_connection.execute('''
            select 
                p."user_id",
                f."feature_id",
                i."image_type",
                f."created_at" as "feature_created_at",
                g."grant",
                g."created_at" as "grant_created_at",
                p."created_at" as "user_created_at"
            from (
                select 
                    "user_id",
                    "created_at" 
                from "User" 
                order by "user_id", "created_at"
                limit ? offset ?) p
            left outer join "Feature" f on f."user_id" = p."user_id"
            left outer join "Image" i on i."image_id" = f."image_id"
            left outer join "Grant" g on g."user_id" = p."user_id"
            order by p."user_id", p."created_at"
        ''', parameters=[limit, offset]) as cursor:
            current_user_features: User = None
            async for row in cursor:
                row_user_id = uuid.UUID(row['user_id'])

                if not current_user_features:
                    current_user_features = User(row_user_id, UserFeatures(row_user_id, []), grants=[], created_at=datetime.datetime.fromisoformat(row['user_created_at']))
                if current_user_features.idx != row_user_id:
                    yield current_user_features
                    current_user_features = User(row_user_id, UserFeatures(row_user_id, []), grants=[], created_at=datetime.datetime.fromisoformat(row['user_created_at']))

                if row['grant'] and not(row['grant'] in current_user_features.grants):
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

    async def get_pooled_connection_or_transaction_connection(self, transaction_scope= None) -> aiosqlite.Connection:
        pooled_connection = transaction_scope if transaction_scope else self.__pooled_connection

        if not pooled_connection:
            pooled_connection = self.__pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            pooled_connection.row_factory = aiosqlite.Row
        
        return pooled_connection

    async def migrations(self) -> None:
        async with aiosqlite.connect(self.__sqlite_file) as db:
            
            for migration_script in migration_scripts:
                await db.execute(migration_script)
            
            await db.commit()
