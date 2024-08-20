
from fastapi import FastAPI, Depends, HTTPException, status

from app.db import USER_DATA
from app.models import Roles, UserRequest
from app.security import create_jwt_token, get_current_active_user, get_current_user
from app.services import get_user, auth_user


app = FastAPI()

@app.post("/login")
def login(user_in: UserRequest):
    authenticated_user = auth_user(user_in.username, user_in.password)
    if authenticated_user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {
        "access_token": create_jwt_token(authenticated_user),
        "token_type": "bearer"
    }

# Доступ любому пользователю
@app.get("/user")
def read_user_data(auth_user: str = Depends(get_current_user)):
    return {"message": "Hello, user!", "user": auth_user.username}

@app.get("/admin")
def read_user_admin_data(auth_user: str = Depends(get_current_active_user)):
    return {"message": "Welcome, admin!", "user": auth_user.username}