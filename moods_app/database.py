from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import dotenv_values
from pathlib import Path


def get_filesystem_db_engine():
    config = dotenv_values(Path(__file__).parent / ".env")
    db_path = (Path(__file__).parent / config["SQLITE_DATABASE_PATH"]).absolute()
    return create_engine(f"sqlite:////{db_path}")  # filesystem db


def get_scoped_session(engine):
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def init_db(engine):
    # initialize the database - uses imported models to create tables/schema
    from moods_app.resources.user import User
    from moods_app.resources.mood_capture import MoodCapture
    from moods_app.resources.base import Base

    Base.metadata.create_all(bind=engine)
