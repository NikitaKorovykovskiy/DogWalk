from fastapi import FastAPI, Depends, HTTPException

from app.db import USER_DATA
from app.models import UserRequest
from app.security import create_jwt_token
from app.services import get_user, auth_user


app = FastAPI()

app.get("/login")
def login(user_in: UserRequest):
    authenticated_user = auth_user(user_in.username, user_in.password)
    if authenticated_user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {
        "access_token": create_jwt_token(authenticated_user),
        "token_type": "bearer"
    }

