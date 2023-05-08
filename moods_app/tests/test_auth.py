from moods_app.auth import authenticate_user
from moods_app.resources.user import User

def test_authentication_success(session):
    user = User(api_key="password")
    session.add(user)
    session.commit()

    auth_error = authenticate_user(
        user_id=user.id,
        api_key="password",
        session=session,
    )
    assert auth_error is None


def test_authentication_failure_no_user(session):
    auth_error = authenticate_user(
        user_id=123,
        api_key="password",
        session=session,
    )
    assert auth_error[1] == 404
    assert auth_error[0] == "User 123 does not exist."


def test_authentication_failure_incorrect_api_key(session):
    user = User(api_key="correct")
    session.add(user)
    session.commit()

    auth_error = authenticate_user(
        user_id=user.id,
        api_key="incorrect",
        session=session,
    )
    assert auth_error[1] == 401
    assert auth_error[0] == f"Invalid api key for user {user.id}."
