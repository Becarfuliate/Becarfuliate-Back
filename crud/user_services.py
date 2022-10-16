from models.entities import User
from pony.orm import db_session, commit
from schemas.iuser import User_create
from cryptography.fernet import Fernet
from decouple import config
import random


KEY_CRYPT = config("KEY")


@db_session()
def add_user(new_user: User_create):
    crypt_fun = Fernet(KEY_CRYPT.encode())
    password_encript = crypt_fun.encrypt((new_user.password).encode())
    password_encript = password_encript.decode()
    code_for_validation = "".join(random.sample(password_encript[7:13], 6))
    with db_session:
        try:
            User(
                username=new_user.username,
                password=password_encript,
                avatar=new_user.avatar,
                confirmation_mail=False,
                email=new_user.email,
                validation_code=code_for_validation,
            )
            commit()
        except Exception as e:
            return str(e)
        return "added"


@db_session
def update_confirmation(username: str, code: str):
    user_for_validate = User[username]
    print(user_for_validate.validation_code)
    if code == user_for_validate.validation_code:
        User[username].confirmation_mail = True
        return "confirmed"
    else:
        return "error"


@db_session
def get_code_for_user(username: str):
    return User[username].validation_code
