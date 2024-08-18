from fastapi.security import OAuth2PasswordBearer
import jwt

from app import config


oauth = OAuth2PasswordBearer(tokenUrl="login")



def create_jwt_token(user):
    data = {
        "username": user.username,
        "role": user.roles
    }

    return jwt.encode(data, config.SECRET_KEY, algorithm=config.ALGORITHM)

def decode_jwt_token(token):
    return jwt.decode(token, "secret", algorithms=["HS256"])