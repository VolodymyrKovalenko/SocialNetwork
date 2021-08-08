from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100))

    posts = relationship("Post", backref="users")

    def __init__(self, email, hashed_password):
        self.email = email
        self.hashed_password = hashed_password

    def __repr__(self):
        return f"<User {self.email}>"