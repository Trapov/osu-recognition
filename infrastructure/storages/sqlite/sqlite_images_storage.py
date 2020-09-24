import logging
import uuid
from typing import AsyncIterator

import aiosqlite

from abstractions.storages import ImagesStorage
from .sqlite_migrations import migration_scripts
import asyncio
from datetime import datetime


class SqliteImagesStorage(ImagesStorage):
    def __init__(self, sqlite_file: str):
        self.__sqlite_file: str = sqlite_file
        self.__pooled_connection : aiosqlite.Connection = None
        
        asyncio.create_task(self.migrations()).add_done_callback(lambda _ : logging.info('Images migrations done'))

    async def save(self, person_id: uuid.UUID, image_type: str, feature_id: uuid.UUID, image: bytes, transaction_scope = None) -> None:
        pooled_connection = transaction_scope if transaction_scope else self.__pooled_connection
        
        if not pooled_connection:
            pooled_connection = self.__pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            pooled_connection.row_factory = aiosqlite.Row

        await pooled_connection.execute('insert or replace into "Image" ("image_id", "image_type", "image", "created_at") values(?, ?, ?, ?)',
            parameters=[str(feature_id), str(image_type), image, str(datetime.utcnow())])
        
        if not transaction_scope:
            await pooled_connection.commit()

    async def delete(self, person_id: uuid.UUID, feature_id: uuid.UUID, transaction_scope = None) -> None:
        pooled_connection = transaction_scope if transaction_scope else self.__pooled_connection

        if not pooled_connection:
            pooled_connection = self.__pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            pooled_connection.row_factory = aiosqlite.Row

        await pooled_connection.execute('''
            PRAGMA foreign_keys = ON;
        ''')
        await pooled_connection.execute('''
            delete from "Image"  
            where "image_id"= ?
        ''', parameters=[str(feature_id)]
        )

        if not transaction_scope:
            await pooled_connection.commit()


    async def get(self, person_id: uuid.UUID, feature_id: uuid.UUID):
        if not self.__pooled_connection:
            self.__pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            self.__pooled_connection.row_factory = aiosqlite.Row

        row = None
        async with self.__pooled_connection.execute('''
                select "image"
                from "Image"
                where "image_id" = ?
            ''', [str(feature_id)]) as cursor:
            row = (await cursor.fetchone())[0]
        
        return row

    async def delete_for_user(self, person_id: uuid.UUID, transaction_scope = None) -> None:
        ...

    async def migrations(self) -> None:
        async with aiosqlite.connect(self.__sqlite_file) as db:

            for migration_script in migration_scripts:
                await db.execute(migration_script)
            
            await db.commit()
