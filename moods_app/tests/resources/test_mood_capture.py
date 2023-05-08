from moods_app.resources.base import Base
from moods_app.resources.mood_capture import MoodCapture, Mood

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite://")

class TestMoodCapture:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = Session(engine)
        self.capture1 = MoodCapture(user_id=123, latitude=71.5, longitude=123.2, mood=Mood.sad)
        self.capture2 = MoodCapture(user_id=456, latitude=23.2, longitude=-100, mood=Mood.happy)
        self.capture3 = MoodCapture(user_id=456, latitude=22.8, longitude=-99, mood=Mood.neutral)
        self.capture4 = MoodCapture(user_id=456, latitude=23.3, longitude=-101, mood=Mood.happy)

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_create_new_mood_capture(self):
        capture = MoodCapture.create_new_mood_capture(
            user_id=123,
            latitude=24.1,
            longitude=-20.5,
            mood=Mood.happy,
            session=self.session,
        )

        in_db = self.session.query(MoodCapture).filter(MoodCapture.id==capture.id).all()
        assert len(in_db) == 1
        assert in_db[0].id == capture.id
        assert in_db[0].user_id == capture.user_id
        assert in_db[0].latitude == capture.latitude
        assert in_db[0].longitude == capture.longitude
        assert in_db[0].mood == capture.mood
    
    def test_get_all_moods_for_user(self):
        self.session.add_all([self.capture1, self.capture2, self.capture3, self.capture4])
        self.session.commit()

        results = MoodCapture.get_all_moods_for_user(user_id=456, session=self.session)

        # make sure we get what we expect!
        assert sorted(results, key=lambda mood: mood.name) == [Mood.happy, Mood.happy, Mood.neutral]

    def test_get_locations_of_happy_moods_for_user(self):
        self.session.add_all([self.capture1, self.capture2, self.capture3, self.capture4])
        self.session.commit()

        results = MoodCapture.get_locations_of_happy_moods_for_user(user_id=456, session=self.session)

        assert sorted(results) == sorted([(23.2, -100), (23.3, -101)])
