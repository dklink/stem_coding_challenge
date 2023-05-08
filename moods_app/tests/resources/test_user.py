from moods_app.resources.base import Base
from moods_app.resources.user import User

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

class TestUser:
    def setup_class(self):
        engine = create_engine("sqlite://")
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_create_user(self):
        """make sure it creates a non-empty api key, and make sure it persists the user into the db"""
        user = User.create_new_user(session=self.session)

        assert isinstance(user.api_key, str)
        assert len(user.api_key)

        in_db = self.session.query(User).filter(User.id==user.id).all()
        assert len(in_db) == 1
        assert in_db[0].id == user.id
        assert in_db[0].api_key == user.api_key
