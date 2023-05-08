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


def test_get_mood_distribution_improper_input(client):
    """ensure the endpoint is checking the input"""
    response = client.post(
        "/mood-captures",
        data={"user_id": "this should be an integer"},
        headers={"x-api-key": "123"},
    )
    assert response._status_code == 400

def test_get_mood_distribution(client):
    pass

def test_get_nearest_happy_location(client):
    pass

