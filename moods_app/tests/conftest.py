import pytest
import warnings
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SAWarning
from sqlalchemy import create_engine
from moods_app.resources.mood_capture import MoodCapture, Mood
from moods_app.resources.user import User
from moods_app.resources.base import Base


# sqlite doesn't enforce foreign key constraints by default; this makes it do so.
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.fixture(scope="session")
def engine():
    """single in-memory db engine to use for all the tests"""
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def session(engine):
    """creates a session to connect to the db, but wraps it in a transaction
    when we rollabck the transaction, it returns the db to a totally clean state,
    even if we've made commits on the session."""
    connection = engine.connect()
    transaction = connection.begin()
    session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    yield session
    session.close()

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=SAWarning)
        transaction.rollback()  # this creates a warning if rollback has already occurred, e.g. because of IntegrityError
    connection.close()
