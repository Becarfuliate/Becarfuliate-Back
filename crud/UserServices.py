from select import select
from models.Users import User
from pony.orm import db_session, select
from schemas.IUser import User_create

@db_session()
def add_user(new_user: User_create):
    User(username=new_user.username,
    password=new_user.password,
    avatar=new_user.avatar,
    email=new_user.email)


@db_session()
def show_user():
    # with db_session
    return "Nada"
