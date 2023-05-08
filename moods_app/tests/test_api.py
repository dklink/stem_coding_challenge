import pytest
from moods_app import api
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from moods_app.resources.base import Base
from moods_app.resources.mood_capture import MoodCapture, Mood
from moods_app.resources.user import User

engine = create_engine(f"sqlite://")  # in memory db, for all tests to access


@pytest.fixture
def client():
    Base.metadata.create_all(engine)  # initialize the db
    
    app = api.create_app(test_config={"TESTING": True, "TEST_DB_ENGINE": engine})
    with app.test_client() as client:
        yield client
    
    Base.metadata.drop_all(engine)  # tear down the db


def test_add_user_response(client):
    """test adding a user provides expected response"""
    response = client.post("/users")

    assert "api_key" in response.json
    assert isinstance(response.json["api_key"], str)
    assert len(response.json["api_key"]) > 0

    assert "user_id" in response.json
    assert isinstance(response.json["user_id"], int)


def test_add_user_persist(client):
    """test that calling the add user endpoint actually adds a user to the db"""
    with Session(engine) as session:
        result = session.query(User).all()
    assert len(result) == 0

    response = client.post("/users")

    with Session(engine) as session:
        result = session.query(User).all()
    assert len(result) == 1
    assert result[0].id == response.json["user_id"]
    assert result[0].api_key == response.json["api_key"]


def test_add_two_users_unique(client):
    """test two users get created with unique IDs and api keys"""
    response1 = client.post("/users")
    response2 = client.post("/users")

    assert response1.json["user_id"] != response2.json["user_id"]
    assert response1.json["api_key"] != response2.json["api_key"]


def test_add_moodcapture(client):
    pass

def test_get_mood_distribution(client):
    pass

def test_get_nearest_happy_location(client):
    pass
