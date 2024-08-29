
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from app.db import USER_DATA
from app.models1 import Roles, UserRequest
from app.security import create_jwt_token, get_current_active_user, get_current_user
from app.services import get_user, auth_user


app = FastAPI()


# не изменяли
class ItemsResponse(BaseModel):
    item_id: int
    

# ДОБАВИЛИ модель пидантика для ошибок  
class CustomExceptionModel(BaseModel):
    status_code: int
    er_message: str
    er_details: str
    kek:str

class CustomExceptionA(HTTPException):
    def __init__(self, detail: str, status_code: int, message: str, kek: str):
        super().__init__(status_code=status_code, detail=detail)
        self.message = message
        self.kek = kek
    
@app.exception_handler(CustomExceptionA)
async def custom_exception_handler(request: Request, exc: CustomExceptionA):
    error = jsonable_encoder(CustomExceptionModel(
        status_code=exc.status_code,
        er_message=exc.detail,
        er_details=exc.message,
        kek=exc.kek
    )
)
    return JSONResponse(status_code=exc.status_code, content=error)


# не изменяли
@app.get(
    path="/items/{item_id}/",
    response_model=ItemsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Items by ID.",
    description="The endpoint returns item_id by ID. If the item_id is 42, an exception with the status code 404 is returned.",
    responses={
        status.HTTP_200_OK: {'model': ItemsResponse},
        status.HTTP_404_NOT_FOUND: {"model": CustomExceptionModel},
    }
)
async def read_item(item_id: int):
    if item_id == 42:
        raise CustomExceptionA(detail="Item not found", status_code=404, message="You're trying to get an item that doesn't exist. Try entering a different item_id.", kek="kek")
    raise CustomExceptionA




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