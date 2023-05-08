from moods_app.resources.base import Base
from moods_app.resources.user import User


def test_create_user(session):
    """make sure it creates a non-empty api key, and make sure it persists the user into the db"""
    user = User.create_new_user(session=session)
    assert user.id == 1

    assert isinstance(user.api_key, str)
    assert len(user.api_key)

    in_db = session.query(User).filter(User.id==user.id).all()
    assert len(in_db) == 1
    assert in_db[0].id == user.id
    assert in_db[0].api_key == user.api_key

def test_get_user_by_id(session):
    user = User(api_key="123")
    session.add(user)
    session.commit()
    assert user.id == 1

    result = User.get_user_by_id(user_id=1, session=session)
    assert result is not None
    assert result.id == user.id
    
def test_get_user_by_id_not_found(session):
    result = User.get_user_by_id(user_id=123, session=session)
    assert result is None
