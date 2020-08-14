from datetime import datetime

class ResizeFactors(object):
    def __init__(self, x = 0.3, y = 0.3):
        self.x = x
        self.y = y

class RecognitionSettings(object):
    def __init__(
        self,
        name: str = "default",
        is_active : bool = False,
        max_features : int = 10,
        base_threshold : float = 0.64,
        rate_of_decreasing_threshold_with_each_feature: float = 0.03,
        created_at : datetime = datetime.utcnow(),
        updated_at: datetime = None,
        resize_factors: ResizeFactors = ResizeFactors()
    ):
        self.name = name
        self.is_active = is_active
        self.max_features = max_features
        self.base_threshold = base_threshold
        self.rate_of_decreasing_threshold_with_each_feature = rate_of_decreasing_threshold_with_each_feature
        self.created_at = created_at
        self.updated_at = updated_at
        self.resize_factors = resize_factors