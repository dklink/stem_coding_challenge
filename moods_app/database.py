from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from moods_app.resources.base import Base

engine = create_engine(f"sqlite:///database/sqlite.db")  # filesystem db

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from resources.user import User
    from resources.mood_capture import MoodCapture
    Base.metadata.create_all(bind=engine)
