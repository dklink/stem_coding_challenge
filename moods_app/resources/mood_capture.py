import enum
from sqlalchemy import Column, Integer, ForeignKey, Float, Enum, select
from moods_app.resources.base import Base
from sqlalchemy.orm import Session


class Mood(enum.Enum):
    happy, sad, neutral = range(3)


class MoodCapture(Base):
    __tablename__ = "mood_captures"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    mood = Column(Enum(Mood), nullable=False)

    @classmethod
    def create_new_mood_capture(
        cls,
        user_id: int,
        latitude: float,
        longitude: float,
        mood: Mood,
        session: Session,
    ):
        mood_capture = MoodCapture(
            user_id=user_id,
            latitude=latitude,
            longitude=longitude,
            mood=mood,
        )
        session.add(mood_capture)
        session.commit()
        return mood_capture

    @classmethod
    def get_all_moods_for_user(cls, user_id: int, session: Session):
        return session.scalars(
            select(MoodCapture.mood).where(MoodCapture.user_id == user_id)
        ).all()

    @classmethod
    def get_locations_of_happy_moods_for_user(cls, user_id: int, session: Session):
        return session.execute(
            select(MoodCapture.latitude, MoodCapture.longitude).where(
                MoodCapture.user_id == user_id,
                MoodCapture.mood == Mood.happy,
            )
        ).all()
