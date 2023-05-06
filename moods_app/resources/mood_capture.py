import enum
from sqlalchemy import Column, Integer, Float, Enum
from sqlalchemy.orm import declarative_base


class Mood(enum.Enum):
    HAPPY = "happy"
    SAD = "sad"
    NEUTRAL = "neutral"


Base = declarative_base()

class MoodCapture(Base):
    __tablename__ = 'mood_captures'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    mood = Column(Enum(Mood))
