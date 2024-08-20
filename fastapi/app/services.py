from app.db import USER_DATA
from app.hash_password import verify_password
from app.models1 import User


def get_user(username: str) -> User|None:
    for user in USER_DATA:
        if username != user["username"]:
            continue
        else:
            return User(**user)
    return None
    
    

def auth_user(username: str, password: str) -> User|None:
    user = get_user(username)
    if user is None or not verify_password(password, user.password):
        return None
    return user
