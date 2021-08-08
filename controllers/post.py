from models.post import Post
from schemas import PostCreate as PostCreateSchema
from models.database import SessionLocal

db = SessionLocal()


class PostController:

    @staticmethod
    async def get_posts(skip: int = 0, limit: int = 100):
        return db.query(Post).offset(skip).limit(limit).all()

    @staticmethod
    async def create_user_post(post: PostCreateSchema, user_id: int):
        post = Post(
            title=post.title, description=post.description, liked=0, disliked=0, user_id=user_id
        )
        db.add(post)
        db.commit()
        return post

    @staticmethod
    async def like_post(post_id: int):
        post = db.query(Post).filter(Post.id == post_id).first()
        post.liked += 1
        db.commit()
        return post

    @staticmethod
    async def dislike_post(post_id: int):
        post = db.query(Post).filter(Post.id == post_id).first()
        post.disliked += 1
        db.commit()
        return post

