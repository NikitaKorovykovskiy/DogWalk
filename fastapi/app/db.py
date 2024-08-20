
from app.hash_password import hash_password
from app.models import Roles


USER_DATA = [
    {"username": "admin", "password": hash_password("admin"), "role": Roles.ADMIN},
    {"username": "user", "password": hash_password("password"), "role": Roles.USER},
    {"username": "guest", "password": hash_password("12345"), "role": Roles.GUEST}
]