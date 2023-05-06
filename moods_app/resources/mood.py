from enum import Enum


class Mood(Enum):
    HAPPY = "happy"
    SAD = "sad"
    NEUTRAL = "neutral"


class MoodCapture:
    """Represents a mood capture from our shiny new phone camera."""

    def __init__(
            self,
            user_id: int,
            longitude: float,
            latitude: float,
            mood: Mood,
            ):
        self.user_id = user_id
        self.longitude = longitude
        self.latitude = latitude
        self.mood = mood
