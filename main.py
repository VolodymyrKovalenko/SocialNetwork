from typing import List

import schemas
from fastapi import Depends, FastAPI, HTTPException
from controllers.post import PostController
from controllers.user import UserController
from authentication import Auth
auth_handler = Auth()

app = FastAPI()


@app.post("/login", response_model=schemas.AuthToken)
async def login_user(user: schemas.UserAuthenticate):
    db_user = await UserController.get_user_by_email(email=user.email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Email is incorrect")
    else:
        is_password_correct = await UserController.check_user_password(user)
        if not is_password_correct:
            raise HTTPException(status_code=400, detail="Password is not correct")
        else:
            access_token = auth_handler.encode_token(user.email)
            return {"access_token": access_token}


@app.post("/signup", response_model=schemas.SignUpUser, status_code=201)
async def signup(user: schemas.UserAuthenticate):
    db_user = await UserController.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User with this email already registered")
    user = await UserController.create_user(user=user)
    user_data = schemas.User.from_orm(user).dict()
    user_data["access_token"] = auth_handler.encode_token(user.email)
    return user_data


@app.get("/users/{email}", response_model=schemas.User)
async def get_user_by_email(email: str, access_token: schemas.AuthToken = Depends(auth_handler.verify_token)):
    db_user = await UserController.get_user_by_email(email=email)
    if not db_user:
        raise HTTPException(status_code=404, detail="There is no user with this email")
    return db_user


@app.get("/users/", response_model=List[schemas.User])
async def get_users(skip: int = 0, limit: int = 100):
    users = await UserController.get_users(skip=skip, limit=limit)
    return users


@app.post("/users/{user_id}/posts/", response_model=schemas.Post, status_code=201)
async def create_post_for_user(
    user_id: int, post: schemas.PostCreate, access_token: schemas.AuthToken = Depends(auth_handler.verify_token)
):
    return await PostController.create_user_post(post=post, user_id=user_id)


@app.get("/users/{user_id}/posts/", response_model=List[schemas.Post])
async def get_posts_by_user(user_id: int = 0):
    posts = await UserController.get_posts_by_user(user_id=user_id)
    return posts


@app.get("/posts/", response_model=List[schemas.Post])
async def get_all_posts(skip: int = 0, limit: int = 100):
    posts = await PostController.get_posts(skip=skip, limit=limit)
    return posts


@app.patch("/posts/{post_id}/like", response_model=schemas.Post, status_code=200)
async def like_posts(
        post_id: int, access_token: schemas.AuthToken = Depends(auth_handler.verify_token)
):
    return await PostController.like_post(post_id)


@app.patch("/posts/{post_id}/dislike", response_model=schemas.Post, status_code=200)
async def dislike_posts(
        post_id: int, access_token: schemas.AuthToken = Depends(auth_handler.verify_token)
):
    return await PostController.dislike_post(post_id)



