from pydantic import BaseModel
from enum import Enum

class Roles(Enum):
    GUEST = "guest"
    USER = "user"
    ADMIN = "admin"


class User(BaseModel):
    username: str
    password: str
    role: Roles

class UserRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str
    roles: str