from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String(500))
    liked = Column(Integer)
    disliked = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, title, description, liked, disliked, user_id):
        self.title = title
        self.description = description
        self.liked = liked
        self.disliked = disliked
        self.user_id = user_id

    def __repr__(self):
        return f"<Post(title={self.title})>"
