from fastapi import APIRouter
from crud.UserSERvices import *
from schemas.IUser import *
from auth.jwt_handler import *

user_end_points = APIRouter()
@user_end_points.get("/user")
def show_all_users():
    '''
        Esto no hace nada
    '''
    user = show_user()
    return user


@user_end_points.post("/register")
def user_register(user_to_add: User_base):
    add_user(new_user=user_to_add)
    return {"Status": "Usuer added succesfully"}

def check_user(user:user_login_schema):
    data = search_user(user.username,user.email)
    print(data)
    print("pass data",data[0][2])
    print ("pass de user",user.password)
    if (user.password == data[0][2]):
        return True
    else:
        return False

@user_end_points.post("/user/login")
def user_login(user:user_login_schema):
    if (check_user(user)):
        response = sign_JWT(user.email)
        return {"token":response}
    else:
        return {"error":"xd"}



