from abstractions import Page, RecognitionSettings, ResizeFactors
from abstractions.storages import RecognitionSettingsStorage
import datetime

async def handle(
        settings_storage: RecognitionSettingsStorage) -> RecognitionSettings:

    return await settings_storage.get_current()
