# databas3
from select import select
from models.Users import User
from pony.orm import db_session
from schemas.IUser import *
import jwt
from datetime import datetime, timedelta
from decouple import (
    config,
)

# se obtienen de env
JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")
JWT_EXPIRES = timedelta(1)


# esta funcion encodea el token
def get_payload(userID: str):
    payload = {"userID": userID, "expiry": str(datetime.now() + JWT_EXPIRES)}
    return payload


def sign_JWT(userID: str):
    payload = get_payload(userID)
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


# esta funcion decodea el token
def decode_JWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decode_token
    except:
        return {"userID": "", "expiry": 0}


# inserta un usuario en la base de datos
@db_session()
def add_user(inusername,inpassword,inavatar,inemail):
    User(
        username=inusername,
        password=inpassword,
        avatar=inavatar,
        email=inemail,
    )


# busca un usuario en la base de datos por su nombre
@db_session()
def search_user(name):
    data = User.get(username=name)
    return data

@db_session
def search_user_by_email(input_email):
    data = User.select(lambda p : p.email ==input_email).get()
    print (data)
    return data