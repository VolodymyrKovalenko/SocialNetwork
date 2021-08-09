import asyncio
import logging
import string
import random
import aiohttp
from random import randint
from config import (
    API_URL, NUMBER_OF_USERS,
    MAX_POSTS_PER_USER, MAX_LIKES_PER_USER
)

logging.basicConfig(datefmt='%m/%d/%Y %I:%M:%S %p')


class Bot:
    def __init__(self, api_url, number_of_users, max_posts_per_user, max_likes_per_user):
        self.api_url = api_url
        self.number_of_users = number_of_users
        self.max_posts_per_user = max_posts_per_user
        self.max_likes_per_user = max_likes_per_user

    async def sign_up(self, email, password):
        url = f'{self.api_url}/signup'
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={'email': email, 'password': password}) as resp:
                if resp.status == 201:
                    return await resp.json()

    async def create_post(self, user_id, access_token):
        url = f'{self.api_url}/users/{user_id}/posts/'
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json={
                    'user_id': user_id,
                    'title': generate_random_string(30),
                    'description': generate_random_string(100)
                },
                params={
                    'access_token': access_token
                }
            ) as resp:
                if resp.status == 201:
                    post_data = await resp.json()
                    print(f'Post {post_data["id"]} created by user {user_id}')
                    return post_data

    async def like_post(self, post_id, access_token):
        url = f'{self.api_url}/posts/{post_id}/like'
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                url, json={'id': post_id}, params={'access_token': access_token}
            ) as resp:
                if resp.status == 200:
                    print(f'Post {post_id} has been liked by user')
                return await resp.json()


def generate_random_string(length=20):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


async def main():
    bot = Bot(API_URL, NUMBER_OF_USERS, MAX_POSTS_PER_USER, MAX_LIKES_PER_USER)

    for user in range(NUMBER_OF_USERS):
        email = generate_random_string(20)
        password = generate_random_string(15)

        user_data = await bot.sign_up(email, password)
        access_token = user_data.get("access_token")
        user_id = user_data.get("id")
        for post in range(randint(1, MAX_POSTS_PER_USER)):
            post = await bot.create_post(user_id, access_token)
            post_id = post.get("id")
            if post_id:
                for _ in range(randint(1, MAX_LIKES_PER_USER)):
                    await bot.like_post(post_id, access_token)


if __name__ == '__main__':
    asyncio.run(main())
