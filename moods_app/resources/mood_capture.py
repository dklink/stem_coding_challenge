import enum
from sqlalchemy import Column, Integer, Float, Enum, select
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.engine.base import Engine


class Mood(enum.Enum):
    happy, sad, neutral = range(3)


Base = declarative_base()

class MoodCapture(Base):
    __tablename__ = 'mood_captures'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    mood = Column(Enum(Mood))


### DB QUERY FUNCTIONS
def get_all_moods_for_user(user_id: int, session):
    return session.scalars(
        select(MoodCapture.mood)
        .where(MoodCapture.user_id == user_id)
    ).all()

def get_locations_of_happy_moods_for_user(user_id: int, session):
    return session.execute(
        select(MoodCapture.latitude, MoodCapture.longitude)
        .where(
            MoodCapture.user_id == user_id,
            MoodCapture.mood == Mood.happy,
        )
    ).all()
