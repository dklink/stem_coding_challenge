from moods_app.resources.user import User
from sqlalchemy.orm import Session

def authenticate_user(user_id: int, api_key: str, session: Session):
    """Check the user exists and the api key is correct.
    Returns None on success, (message, code) tuple on failure."""

    if api_key is None:
        return "Missing api key", 400
    elif not isinstance(api_key, str):
        return "Invalid data type: api key must be a string.", 400
    
    user = User.get_user_by_id(user_id=user_id, session=session)
    if user is None:
        return f"User {user_id} does not exist.", 404
    elif user.api_key != api_key:
        return f"Invalid api key for user {user_id}.", 401
    else:
        return None
