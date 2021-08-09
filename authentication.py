import bcrypt
import jwt
from fastapi import HTTPException
from datetime import timedelta, datetime
from settings import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES

ALGORITHM = "HS256"


class Auth:

    @staticmethod
    def encode_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def verify_password(input_password, db_password):
        return bcrypt.checkpw(input_password.encode('utf-8'), db_password)

    @staticmethod
    def encode_token(email, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
        payload = {'data': email}
        expire = datetime.utcnow() + expires_delta
        payload.update({"exp": expire})
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(access_token):
        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload['data']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    @classmethod
    def refresh_token(cls, expired_token):
        try:
            payload = jwt.decode(expired_token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_exp': False})
            email = payload['data']
            new_token = cls.encode_token(email)
            return {'token': new_token}

        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')
