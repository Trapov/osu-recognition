import uuid

import aiosqlite

from abstractions.storages import TransactionContext
import asyncio


class AiosqliteTransactionContext(TransactionContext):

    def __init__(self, sqlite_file: str):
        self.__sqlite_file: str = sqlite_file
        self.pooled_connection : aiosqlite.Connection = None

    async def __aenter__(self):
        if not self.pooled_connection:
            self.pooled_connection = await aiosqlite.connect(self.__sqlite_file)
            self.pooled_connection.row_factory = aiosqlite.Row
            
        return self.pooled_connection

    async def __aexit__(self, exc_type, exc, tb):
        await self.pooled_connection.commit()