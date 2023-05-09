from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import dotenv_values


def get_filesystem_db_engine():
    config = dotenv_values(".env")
    return create_engine(f"sqlite:///{config['SQLITE_DATABASE_PATH']}")  # filesystem db

def get_scoped_session(engine):
    return scoped_session(sessionmaker(autocommit=False,
                                       autoflush=False,
                                       bind=engine))

def init_db(engine):
    # initialize the database - uses imported models to create tables/schema
    from moods_app.resources.user import User
    from moods_app.resources.mood_capture import MoodCapture
    from moods_app.resources.base import Base
    Base.metadata.create_all(bind=engine)
