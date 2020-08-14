import uuid
from abstractions.recognition_settings import RecognitionSettings, ResizeFactors
from abstractions.storages import RecognitionSettingsStorage
import asyncio
import aiosqlite
import logging
from typing import AsyncIterator
from .sqlite_migrations import migration_scripts
import datetime

class SqliteRecognitionSettingsStorage(RecognitionSettingsStorage):
    def __init__(self, sqlite_file: str):
        self.__sqlite_file: str = sqlite_file
        self.__pooled_connection : aiosqlite.Connection = None
        asyncio.create_task(self.migrations()).add_done_callback(lambda _ : logging.info('Recognition settings migrations done'))
        
    async def save(self, settings : RecognitionSettings) -> None:
        if not self.__pooled_connection:
            self.__pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            self.__pooled_connection.row_factory = aiosqlite.Row

        # todo, make constraints
        await self.__pooled_connection.execute('''
            update "RecognitionSetting"
            set "is_active" = 0
            where "is_active" = 1
        ''')

        await self.__pooled_connection.execute('''
            insert or replace into "RecognitionSetting" (
                "name",
                "is_active",
                "max_features",
                "base_threshold",
                "rate_of_decreasing_threshold_with_each_feature",
                "created_at",
                "updated_at",
                "resize_factors_x",
                "resize_factors_y"
            ) values (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',parameters=[
                str(settings.name),
                int(settings.is_active),
                settings.max_features,
                settings.base_threshold,
                settings.rate_of_decreasing_threshold_with_each_feature,
                str(settings.created_at),
                str(settings.updated_at) if settings.updated_at else None,
                settings.resize_factors.x,
                settings.resize_factors.y
            ]
        )

        await self.__pooled_connection.commit()

    async def get_current(self) -> RecognitionSettings:
        if not self.__pooled_connection:
            self.__pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            self.__pooled_connection.row_factory = aiosqlite.Row

        async with self.__pooled_connection.execute('''
            select                 
                "name",
                "is_active",
                "max_features",
                "base_threshold",
                "rate_of_decreasing_threshold_with_each_feature",
                "created_at",
                "updated_at",
                "resize_factors_x",
                "resize_factors_y"
            from "RecognitionSetting"
            where "is_active" = 1
        ''') as cursor:
            r = (await cursor.fetchone())
            return RecognitionSettings(
                    name=r["name"],
                    is_active=r["is_active"],
                    max_features=r["max_features"],
                    base_threshold = r["base_threshold"],
                    rate_of_decreasing_threshold_with_each_feature = r["rate_of_decreasing_threshold_with_each_feature"],
                    created_at = datetime.datetime.fromisoformat(r["created_at"]),
                    updated_at = datetime.datetime.fromisoformat(r["updated_at"]) if r["updated_at"] else None,
                    resize_factors = ResizeFactors(x=r["resize_factors_x"],y=r["resize_factors_x"])
                )

    async def get(self, name : str = RecognitionSettings().name) -> RecognitionSettings:
        if not self.__pooled_connection:
            self.__pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            self.__pooled_connection.row_factory = aiosqlite.Row

        async with self.__pooled_connection.execute('''
            select                 
                "name",
                "is_active",
                "max_features",
                "base_threshold",
                "rate_of_decreasing_threshold_with_each_feature",
                "created_at",
                "updated_at",
                "resize_factors_x",
                "resize_factors_y"
            from "RecognitionSetting"
            where "name" = ?
        ''', parameters=[name]) as cursor:
            r = (await cursor.fetchone())
            return RecognitionSettings(
                    name=r["name"],
                    is_active=r["is_active"],
                    max_features=r["max_features"],
                    base_threshold = r["base_threshold"],
                    rate_of_decreasing_threshold_with_each_feature = r["rate_of_decreasing_threshold_with_each_feature"],
                    created_at = datetime.datetime.fromisoformat(r["created_at"]),
                    updated_at = datetime.datetime.fromisoformat(r["updated_at"]) if r["updated_at"] else None,
                    resize_factors = ResizeFactors(x=r["resize_factors_x"],y=r["resize_factors_x"])
                )

    async def count(self) -> int:
        if not self.__pooled_connection:
            self.__pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            self.__pooled_connection.row_factory = aiosqlite.Row

        async with self.__pooled_connection.execute('''
            select count(1)
            from "RecognitionSetting" p
        ''') as cursor:
            return (await cursor.fetchone())[0]

    async def enumerate(self, offset: int = None, limit: int = None) -> AsyncIterator[RecognitionSettings]:
        if not self.__pooled_connection:
            self.__pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            self.__pooled_connection.row_factory = aiosqlite.Row

        async with self.__pooled_connection.execute('''
            select                 
                "name",
                "is_active",
                "max_features",
                "base_threshold",
                "rate_of_decreasing_threshold_with_each_feature",
                "created_at",
                "updated_at",
                "resize_factors_x",
                "resize_factors_y"
            from "RecognitionSetting"
            order by "created_at", "updated_at"
            limit ? offset ?
        ''', parameters=[limit, offset]) as cursor:
            async for r in cursor:
                yield RecognitionSettings(
                    name=r["name"],
                    is_active=r["is_active"],
                    max_features=r["max_features"],
                    base_threshold = r["base_threshold"],
                    rate_of_decreasing_threshold_with_each_feature = r["rate_of_decreasing_threshold_with_each_feature"],
                    created_at = datetime.datetime.fromisoformat(r["created_at"]),
                    updated_at = datetime.datetime.fromisoformat(r["updated_at"]) if r["updated_at"] else None,
                    resize_factors = ResizeFactors(x=r["resize_factors_x"],y=r["resize_factors_x"])
                )
                    

    async def migrations(self) -> None:
        async with aiosqlite.connect(self.__sqlite_file) as db:
            
            for migration_script in migration_scripts:
                await db.execute(migration_script)
            
            await db.commit()
