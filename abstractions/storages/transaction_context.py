from abc import ABC, abstractmethod

class TransactionContext(ABC):

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb):
        ...