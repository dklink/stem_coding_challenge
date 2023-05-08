from secrets import token_urlsafe
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from moods_app.resources.base import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    api_key = Column(String, nullable=False)

    @classmethod
    def create_new_user(cls, session: Session):
        api_key = token_urlsafe()
        user = User(api_key=api_key)
        session.add(user)
        session.commit()
        return user

    @classmethod
    def get_user_by_id(cls, user_id: int, session: Session):
        """returns specified user.  If not found, returns None."""
        return session.query(User).where(User.id == user_id).scalar()
