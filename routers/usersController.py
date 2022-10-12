from fastapi import APIRouter
from crud.UserSERvices import search_user
from schemas.IUser import user_login_schema
from auth.jwt_handler import *

user_end_points = APIRouter()

def check_user(user:user_login_schema):
    data = search_user(user.name,user.email)
    if (user.password == data.password):
        return True
    else:
        return False

@user_end_points.post("/user/login",tags=["user"])
def user_login(user:user_login_schema):
    if (check_user(user)):
        return sign_JWT(user.email)
    else:
        return{}



