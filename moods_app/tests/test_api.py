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
    response = client.post("/users").json

    assert set(response.keys()) == {"user_id", "api_key"}
    assert isinstance(response["user_id"], int)
    assert isinstance(response["api_key"], str)
    assert len(response["api_key"]) > 0  # not an empty string


def test_add_user_persist(client):
    """test that calling the add user endpoint actually adds a user to the db"""
    with Session(engine) as session:
        result = session.query(User).all()
    assert len(result) == 0

    response = client.post("/users").json

    with Session(engine) as session:
        result = session.query(User).all()
        assert len(result) == 1
        assert result[0].id == response["user_id"]


def test_add_two_users_unique(client):
    """test two users get created with unique IDs and api keys"""
    response1 = client.post("/users")
    response2 = client.post("/users")

    assert response1.json["user_id"] != response2.json["user_id"]
    assert response1.json["api_key"] != response2.json["api_key"]


'''
def test_add_mood_capture_response(client):
    """test that adding a new mood capture provides the expected response"""
    response = client.post("/mood-captures", data={
        "user_id": 42,
        "latitude": 0.01,
        "longitude": 124.2,
        "mood": "happy",
    })
    response = response.json

    assert isinstance(response["mood_capture_id"], int)
    assert response["user_id"] == 42
    assert response["latitude"] == 0.01
    assert response["longitude"] == 124.2
    assert response["mood"] == "happy"


def test_add_mood_capture_persist(client):
    """test that calling the add mood capture endpoint adds the entity to the db"""
    with Session(engine) as session:
        result = session.query(MoodCapture).all()
    assert len(result) == 0

    

    response1 = client.post("/users")
    

    response = client.post("/mood-captures/", data={
        "user_id": response1.json,
        "latitude": 0.01,
        "longitude": 124.2,
        "mood": "happy",
    }).json

    with Session(engine) as session:
        result = session.query(MoodCapture).all()
        import pdb; pdb.set_trace()
        assert len(result) == 1
        assert result[0].id == response["mood_capture_id"]
'''

def test_add_mood_capture_invalid_entry(client):
    pass

def test_get_mood_distribution(client):
    pass

def test_get_nearest_happy_location(client):
    pass


def test_authentication_success(client):
    with Session(engine) as session:
        user = User(api_key="password")
        session.add(user)
        session.commit()

        auth_error = api.authenticate_user(
            user_id=user.id,
            api_key="password",
            session=session,
        )
        assert auth_error is None
