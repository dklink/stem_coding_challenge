from moods_app.database import init_db
from sqlalchemy import create_engine, inspect

def test_init_db():
    """tests that init_db() creates the expected tables, with the expected column names"""
    engine = create_engine(f"sqlite://")  # create empty database
    assert inspect(engine).get_table_names() == []

    init_db(engine=engine)

    inspector = inspect(engine)
    assert sorted(inspector.get_table_names()) == sorted(["users", "mood_captures"])

    user_columns = [column_info["name"] for column_info in inspector.get_columns("users")]
    mood_capture_columns = [column_info["name"] for column_info in inspector.get_columns("mood_captures")]
    assert sorted(user_columns) == sorted(["id", "api_key"])
    assert sorted(mood_capture_columns) == sorted(["id", "user_id", "latitude", "longitude", "mood"])
