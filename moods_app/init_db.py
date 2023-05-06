"""initializes a new sqlite database using sqlalchemy"""

from resources.mood_capture import *
from sqlalchemy import create_engine

engine = create_engine("sqlite:///database.db", echo=True)
Base.metadata.create_all(engine)
