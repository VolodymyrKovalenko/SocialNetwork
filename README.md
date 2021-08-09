# SocialNetwork

### Steps to init the project
```
cd /path/to/yourproject
python3 -m venv venv
source /venv/bin/activate
pip install -r requirements.txt
alembic init alembic
alembic revision -m "init user, post tables"
alembic upgrade head
```

### Start fast-api
```
uvicorn main:app --reload
```
### Start automated bot
```
cd automated_bot
python bot.py
```