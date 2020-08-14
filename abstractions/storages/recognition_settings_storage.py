import uuid
from ..recognition_settings import RecognitionSettings
from abc import ABC, abstractmethod


class RecognitionSettingsStorage(ABC):

    @abstractmethod
    async def save(self, settings : RecognitionSettings) -> None:
        ...

    @abstractmethod
    async def get(self, name : str = RecognitionSettings().name) -> RecognitionSettings:
        ...

    @abstractmethod
    async def get_current(self) -> RecognitionSettings:
        ...