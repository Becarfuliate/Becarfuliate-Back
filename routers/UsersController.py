from fastapi import APIRouter
from models.Users import User
from crud.UserServices import add_user, show_user
from schemas.IUser import User_base


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
