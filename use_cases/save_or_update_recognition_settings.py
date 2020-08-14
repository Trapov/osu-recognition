from abstractions import Page, RecognitionSettings, ResizeFactors
from abstractions.storages import RecognitionSettingsStorage
import datetime

async def handle(
        name: str,
        is_active : bool,
        max_features : int,
        base_threshold : float,
        rate_of_decreasing_threshold_with_each_feature: float,
        resize_factors_x: float,
        resize_factors_y: float,
        settings_storage: RecognitionSettingsStorage) -> None:

    await settings_storage.save(
        RecognitionSettings(
            name=name,
            is_active=is_active,
            max_features=max_features,
            base_threshold=base_threshold,
            rate_of_decreasing_threshold_with_each_feature=rate_of_decreasing_threshold_with_each_feature,
            resize_factors=ResizeFactors(x=resize_factors_x,y=resize_factors_y),
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
    )
