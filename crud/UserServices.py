from select import select
from click import confirmation_option
from models.Entities import User
from pony.orm import db_session, select, commit
from schemas.IUser import User_create
import json
from cryptography.fernet import Fernet

# from decouple import config


# KEY_CRYPT = config('KEY')

@db_session()
def add_user(new_user: User_create):
    # crypt_fun = Fernet(KEY_CRYPT.encode())
    # password_encript = str(crypt_fun.encrypt((new_user.password).encode()))
    with db_session:
        try:
            User(
                username=new_user.username,
                password=new_user.password,
                avatar=new_user.avatar,
                confirmation_mail=False,
                email=new_user.email
            )
            commit()
        except Exception as e:
            return str(e)
        return "added"
