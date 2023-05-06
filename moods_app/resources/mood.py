class Mood:
    """Represents a mood capture from our shiny new phone camera."""

    def __init__(
            self,
            user_id: int,
            longitude: float,
            latitude: float,
            emotional_state: str,
            ):
        self.user_id = user_id
        self.longitude = longitude
        self.latitude = latitude
        self.emotional_state = emotional_state
