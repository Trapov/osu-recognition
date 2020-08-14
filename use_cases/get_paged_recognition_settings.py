from abstractions import Page, RecognitionSettings
from abstractions.storages import RecognitionSettingsStorage


async def handle(
        offset: int,
        count: int,
        settings_storage: RecognitionSettingsStorage) -> Page[RecognitionSettings]:
    total = await settings_storage.count()

    if total == 0:
        return Page(values=[], offset=offset, total=total)

    values = [value async for value in settings_storage.enumerate(offset=offset, limit=count)]

    return Page(values, offset, total)
