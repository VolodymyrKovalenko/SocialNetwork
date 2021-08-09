from sqlalchemy.orm import Session

import schemas
from models.user import User
from authentication import Auth
from models.database import SessionLocal

db = SessionLocal()


class UserController:

    @staticmethod
    async def get_user(user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    async def get_user_by_email(email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    async def get_users(skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    async def create_user(user: schemas.UserAuthenticate):
        hashed_password = Auth.encode_password(user.password)
        db_user = User(email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        return db_user

    @staticmethod
    async def check_user_password(user: schemas.UserAuthenticate):
        db_user_info: User = await UserController.get_user_by_email(email=user.email)
        return Auth.verify_password(user.password, db_user_info.hashed_password)

    @staticmethod
    async def get_posts_by_user(user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        return user.posts
