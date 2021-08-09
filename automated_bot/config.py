import configparser
import os

env = os.environ

config = configparser.ConfigParser()
config.read('config.ini')

API = config['API']
API_URL = API.get('url')

BOT = config['BOT']
NUMBER_OF_USERS = int(BOT.get('number_of_users'))
MAX_POSTS_PER_USER = int(BOT.get('max_posts_per_user'))
MAX_LIKES_PER_USER = int(BOT.get('max_likes_per_user'))
