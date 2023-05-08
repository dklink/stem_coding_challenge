"""tool to initialize a new sqlite db from our model definitions"""
from pathlib import Path

from moods_app.resources.base import Base
import moods_app.resources.mood_capture
import moods_app.resources.user

from sqlalchemy import create_engine

def init_db():
    db_path = Path(__file__).parent / "database" / "sqlite.db"
    engine = create_engine("sqlite:///" + str(db_path))  #TODO put this path in a env file
    Base.metadata.create_all(engine)
