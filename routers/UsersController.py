from fastapi import APIRouter, HTTPException
from models.Entities import User
from crud.UserServices import add_user
from schemas.IUser import User_base


user_end_points = APIRouter()


@user_end_points.post("/register")
def user_register(user_to_add: User_base):
    msg = add_user(new_user=user_to_add)
    if ('IntegrityError' in msg and 'username' in msg):
        raise HTTPException(
            status_code=409,
            detail="El nombre de usuario ya existe"
            )
    if ('IntegrityError' in msg and 'email' in msg):
        raise HTTPException(
            status_code=409,
            detail="El email ya existe"
            )
    return {"Status": "Usuer added succesfully"}
