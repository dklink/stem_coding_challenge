"""initializes a new sqlite database using sqlalchemy"""

from resources.mood_capture import *
from sqlalchemy import create_engine

engine = create_engine("sqlite:///database.db")  #TODO put this path in a env file
Base.metadata.create_all(engine)
