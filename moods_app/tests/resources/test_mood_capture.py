import pytest
from moods_app.resources.mood_capture import MoodCapture, Mood
from moods_app.resources.user import User
from moods_app.resources.base import Base

from sqlalchemy.exc import IntegrityError


@pytest.fixture()
def session(session):  # overload the fixture
    # insert some fake users for every session, to satisfy foreign key
    user1 = User(api_key="123")
    user2 = User(api_key="456")
    session.add_all([user1, user2])
    session.commit()
    assert user1.id == 1
    assert user2.id == 2
    yield session


@pytest.fixture()
def dummy_captures():
    capture1 = MoodCapture(user_id=1, latitude=71.5, longitude=123.2, mood=Mood.sad)
    capture2 = MoodCapture(user_id=2, latitude=23.2, longitude=-100, mood=Mood.happy)
    capture3 = MoodCapture(user_id=2, latitude=22.8, longitude=-99, mood=Mood.neutral)
    capture4 = MoodCapture(user_id=2, latitude=23.3, longitude=-101, mood=Mood.happy)
    return [capture1, capture2, capture3, capture4]


def test_create_new_mood_capture(session):
    capture = MoodCapture.create_new_mood_capture(
        user_id=1,
        latitude=24.1,
        longitude=-20.5,
        mood=Mood.happy,
        session=session,
    )

    in_db = session.query(MoodCapture).filter(MoodCapture.id == capture.id).all()
    assert len(in_db) == 1
    assert in_db[0].id == 1
    assert in_db[0].user_id == 1
    assert in_db[0].latitude == 24.1
    assert in_db[0].longitude == -20.5
    assert in_db[0].mood == Mood.happy


def test_create_new_mood_capture_no_user(session):
    with pytest.raises(IntegrityError):
        capture = MoodCapture.create_new_mood_capture(
            user_id=42,  # doesn't exist in db
            latitude=0,
            longitude=0,
            mood=Mood.happy,
            session=session,
        )


def test_get_all_moods_for_user(session, dummy_captures):
    session.add_all(dummy_captures)
    session.commit()

    results = MoodCapture.get_all_moods_for_user(user_id=2, session=session)

    # make sure we get what we expect!
    assert sorted(results, key=lambda mood: mood.name) == [
        Mood.happy,
        Mood.happy,
        Mood.neutral,
    ]


def test_get_locations_of_happy_moods_for_user(session, dummy_captures):
    session.add_all(dummy_captures)
    session.commit()

    results = MoodCapture.get_locations_of_happy_moods_for_user(
        user_id=2, session=session
    )

    assert sorted(results) == sorted([(23.2, -100), (23.3, -101)])
