import pytest
from moods_app import api
from sqlalchemy import create_engine

from moods_app.resources.base import Base
from moods_app.resources.mood_capture import MoodCapture, Mood
from moods_app.resources.user import User


@pytest.fixture
def client(session):
    app = api.create_app(test_config={"TESTING": True, "TEST_DB_SESSION": session})
    with app.test_client() as client:
        yield client

@pytest.fixture
def one_user_session(session):
    user = User(api_key="123")
    session.add(user)
    session.commit()
    assert user.id == 1
    yield session

@pytest.fixture
def two_user_session(session):
    user1 = User(api_key="123")
    user2 = User(api_key="456")
    session.add_all([user1, user2])
    session.commit()
    assert user1.id == 1
    assert user2.id == 2
    yield session


"""POST /users"""

def test_add_user_response(client):
    """test adding a user provides expected response"""
    response = client.post("/users").json

    assert set(response.keys()) == {"user_id", "api_key"}
    assert isinstance(response["user_id"], int)
    assert isinstance(response["api_key"], str)
    assert len(response["api_key"]) > 0  # not an empty string

def test_add_user_persist(client, session):
    """test that calling the add user endpoint actually adds a user to the db"""
    result = session.query(User).all()
    assert len(result) == 0

    response = client.post("/users").json

    result = session.query(User).all()
    assert len(result) == 1
    assert result[0].id == response["user_id"]

def test_add_two_users_unique(client):
    """test two users get created with unique IDs and api keys"""
    response1 = client.post("/users")
    response2 = client.post("/users")

    assert response1.json["user_id"] != response2.json["user_id"]
    assert response1.json["api_key"] != response2.json["api_key"]


"""POST /mood-captures"""

def test_add_mood_capture_missing_arg(client):
    """ensure the endpoint is checking for missing args"""
    response = client.post("/mood-captures", data={
        "latitude": "this should be a float",
        "longitude": 124.2,
        "mood": "happy",
    },
        headers={"x-api-key": "123"},
    )
    assert response._status_code == 400
    assert response.text == "Missing mandatory parameter: 'user_id'"

def test_add_mood_capture_improper_input(client):
    """ensure the endpoint is checking the input"""
    response = client.post("/mood-captures", data={
        "user_id": "this should be an integer",
        "latitude": "this should be a float",
        "longitude": 124.2,
        "mood": "happy",
    },
        headers={"x-api-key": "123"},
    )
    assert response._status_code == 400
    assert response.text == "'user_id' must be an integer"

def test_add_mood_capture_no_such_user(client):
    """test that adding a new mood capture provides the expected response"""
    response = client.post("/mood-captures", data={
        "user_id": 1,
        "latitude": 0.01,
        "longitude": 124.2,
        "mood": "happy",
    },
        headers={"x-api-key": "123"},
    )
    assert response._status_code == 404
    assert response.text == "User 1 does not exist."

def test_add_mood_capture_incorrect_api_key(client, one_user_session):
    """test that adding a new mood capture provides the expected response"""
    response = client.post("/mood-captures", data={
        "user_id": 1,
        "latitude": 0.01,
        "longitude": 124.2,
        "mood": "happy",
    },
        headers={"x-api-key": "incorrect"},
    )
    assert response._status_code == 401
    assert response.text == "Invalid api key for user 1."

def test_add_mood_capture_response(client, one_user_session):
    """test that adding a new mood capture provides the expected response"""
    response = client.post("/mood-captures", data={
        "user_id": 1,
        "latitude": 0.01,
        "longitude": 124.2,
        "mood": "happy",
    },
        headers={"x-api-key": "123"},
    )
    
    assert response._status_code == 201
    response = response.json
    assert isinstance(response["mood_capture_id"], int)
    assert response["user_id"] == 1
    assert response["latitude"] == 0.01
    assert response["longitude"] == 124.2
    assert response["mood"] == "happy"

def test_add_mood_capture_persist(client, one_user_session):
    """test that calling the add mood capture endpoint adds the entity to the db"""
    result = one_user_session.query(MoodCapture).all()
    assert len(result) == 0

    response = client.post("/mood-captures", data={
        "user_id": 1,
        "latitude": 0.01,
        "longitude": 124.2,
        "mood": "happy",
    },
        headers={"x-api-key": "123"},
    )
    assert response._status_code == 201

    result = one_user_session.query(MoodCapture).all()
    assert len(result) == 1
    assert result[0].id == response.json["mood_capture_id"]


"""GET /mood-captures/frequency-distribution"""

def test_get_mood_distribution_missing_arg(client):
    """ensure the endpoint is checking for missing args"""
    response = client.get(
        "/mood-captures/frequency-distribution",
        headers={"x-api-key": "123"},
    )
    assert response._status_code == 400
    assert response.text == "Missing mandatory parameter: 'user_id'"

def test_get_mood_distribution_improper_input(client):
    """ensure the endpoint is checking the input"""
    response = client.get(
        "/mood-captures/frequency-distribution?user_id=text",
        headers={"x-api-key": "123"},
    )
    assert response._status_code == 400
    assert response.text == "'user_id' must be an integer"

def test_get_mood_distribution_auth_error(client, one_user_session):
    """ensure the endpoint is doing authentication"""
    response = client.get(
        "/mood-captures/frequency-distribution?user_id=2",
        headers={"x-api-key": "123"},
    )
    assert response._status_code == 404
    assert response.text == "User 2 does not exist."

    response = client.get(
        "/mood-captures/frequency-distribution?user_id=1",
        headers={"x-api-key": "incorrect"},
    )

    assert response._status_code == 401
    assert response.text == "Invalid api key for user 1."

def test_get_mood_distribution_no_captures(client, one_user_session):
    response = client.get(
        "/mood-captures/frequency-distribution?user_id=1",
        headers={"x-api-key": "123"},
    )

    assert response._status_code == 404
    assert response.text == "No mood captures found for this user"

def test_get_mood_distribution(client, two_user_session):
    captures = [
        MoodCapture(user_id=1, latitude=0, longitude=0, mood=Mood.happy),
        MoodCapture(user_id=1, latitude=0, longitude=0, mood=Mood.sad),
        MoodCapture(user_id=1, latitude=0, longitude=0, mood=Mood.neutral),
        MoodCapture(user_id=1, latitude=0, longitude=0, mood=Mood.neutral),
        MoodCapture(user_id=1, latitude=0, longitude=0, mood=Mood.neutral),
        MoodCapture(user_id=2, latitude=0, longitude=0, mood=Mood.happy),
    ]
    two_user_session.add_all(captures)
    two_user_session.commit()

    response = client.get(
        "/mood-captures/frequency-distribution?user_id=1",
        headers={"x-api-key": "123"},
    )
    assert response._status_code == 200
    assert response.json == {
        "happy": 1,
        "neutral": 3,
        "sad": 1,
    }


"""GET /mood_captures/nearest-happy"""

def test_get_nearest_happy_location_missing_arg(client):
    """ensure the endpoint is checking for missing args"""
    response = client.get(
        "/mood-captures/nearest-happy?user_id=1&latitude=0",
        headers={"x-api-key": "123"},
    )
    assert response._status_code == 400
    assert response.text == "Missing mandatory parameter: 'longitude'"

def test_get_nearest_happy_location_improper_input(client):
    """ensure the endpoint is checking the input"""
    response = client.get(
        "/mood-captures/nearest-happy?user_id=text&latitude=0&longitude=0",
        headers={"x-api-key": "123"},
    )

    assert response._status_code == 400
    assert response.text == "'user_id' must be an integer"

def test_get_nearest_happy_location_bad_auth(client, one_user_session):
    """ensure auth is being checked"""
    response = client.get(
        "/mood-captures/nearest-happy?user_id=2&latitude=0&longitude=0",
        headers={"x-api-key": "123"},
    )
    assert response._status_code == 404
    assert response.text == "User 2 does not exist."

    response = client.get(
        "/mood-captures/nearest-happy?user_id=1&latitude=0&longitude=0",
        headers={"x-api-key": "incorrect"},
    )
    assert response._status_code == 401
    assert response.text == "Invalid api key for user 1."

def test_get_nearest_happy_location_no_happy_captures(client, one_user_session):
    """ensure proper response if no happy captures are found for the user"""
    capture = MoodCapture(user_id=1, latitude=0, longitude=0, mood=Mood.sad)
    one_user_session.add(capture)
    one_user_session.commit()

    response = client.get(
        "/mood-captures/nearest-happy?user_id=1&latitude=0&longitude=0",
        headers={"x-api-key": "123"},
    )
    assert response._status_code == 404
    assert response.text == "No happy mood captures found for this user"

def test_get_nearest_happy_location(client, two_user_session):
    """test functionality in normal case"""
    captures = [
        MoodCapture(user_id=1, latitude=10, longitude=10, mood=Mood.happy),
        MoodCapture(user_id=1, latitude=-10, longitude=-10, mood=Mood.happy),
        MoodCapture(user_id=1, latitude=-4, longitude=4, mood=Mood.happy),
        MoodCapture(user_id=1, latitude=0, longitude=-5, mood=Mood.happy),
        MoodCapture(user_id=1, latitude=0, longitude=0, mood=Mood.sad),
        MoodCapture(user_id=2, latitude=1, longitude=1, mood=Mood.happy),
    ]
    two_user_session.add_all(captures)
    two_user_session.commit()

    response = client.get(
        "/mood-captures/nearest-happy?user_id=1&latitude=0&longitude=0",
        headers={"x-api-key": "123"},
    )
    
    assert response._status_code == 200
    assert response.json == {
        "latitude": 0,
        "longitude": -5,
    }
