from moods_app.resources.user import User
from sqlalchemy.orm import Session

def authenticate_user(user_id: int, api_key: str, session: Session):
    """Check the user exists and the api key is correct.
    Returns None on success, (message, code) tuple on failure."""
    user = User.get_user_by_id(user_id=user_id, session=session)
    if user is None:
        return f"User {user_id} does not exist.", 404
    elif user.api_key != api_key:
        return f"Invalid api key for user {user_id}.", 401
    else:
        return None
