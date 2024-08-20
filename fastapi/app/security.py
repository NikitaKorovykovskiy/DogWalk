from fastapi.security import OAuth2PasswordBearer
from app.db import USER_DATA
from app.models1 import Roles, User, UserResponse
import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from app import config


oauth = OAuth2PasswordBearer(tokenUrl="login")


def create_jwt_token(user):
    data = {
        "username": user.username,
        "role": user.role.value
    }

    return jwt.encode(data, config.SECRET_KEY, algorithm=config.ALGORITHM)

def decode_jwt_token(token):
    return jwt.decode(token, "secret", algorithms=["HS256"])


def get_current_user(auth_user: str = Depends(oauth)) -> UserResponse:
    decode_token = decode_jwt_token(auth_user)
    user_name = decode_token.get("username")
    user_data = next((user for user in USER_DATA if user["username"] == user_name), None)
    if not user_data:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    return User(**user_data)
    
def get_current_active_user(current_user: dict = Depends(get_current_user)):
    if current_user.role != Roles.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user