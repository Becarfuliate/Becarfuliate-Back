from fastapi import APIRouter, HTTPException
from crud.UserSERvices import *
from schemas.IUser import *

user_end_points = APIRouter()


@user_end_points.post("/register")
async def user_register(user_to_add: User_base):
    add_user(new_user=user_to_add)
    return {"Status": "Usuer added succesfully"}


@user_end_points.post("/login")
async def user_login(input: user_login_schema):
    data = search_user(input.username)

    if data is None:
        raise HTTPException(status_code=400, detail="no existe el usuario")
    else:
        mail_is_verificated = data.confirmation_mail
        password_is_correct = input.password == data.password

        if not mail_is_verificated:
            raise HTTPException(status_code=400, detail="email no verificado")
        elif not password_is_correct:
            raise HTTPException(status_code=400, detail="contrasenia incorrecta")
        else:
            response = sign_JWT(input.username)
            return {"token": response}
