from telnetlib import AUTHENTICATION
from fastapi import APIRouter, HTTPException, BackgroundTasks
from models.Entities import User
from crud.UserServices import add_user, update_confirmation, get_code_for_user
from schemas.IUser import User_base
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from decouple import config

user_end_points = APIRouter()


@user_end_points.post("/register")
async def user_register(user_to_add: User_base):
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
    code_validation = get_code_for_user(user_to_add.username)
    await send_confirmation_mail(
        user_to_add.email,
        code_validation,
        user_to_add.username
        )
    return {"Status": "Usuer added succesfully"}


@user_end_points.get("/verify")
def user_verification(username: str, code: str):
    update_confirmation(username,code)

MAIL_USERNAME_S = config('MAIL_USERNAME')
MAIL_PASSWORD_S = config('MAIL_PASSWORD')
MAIL_PORT_S = config('MAIL_PORT')
MAIL_SERVER_S = config('MAIL_SERVER')

async def send_confirmation_mail(
    email: str,
    code_validation: str,
    username: str
    ):
    conf = ConnectionConfig(
        MAIL_USERNAME=MAIL_USERNAME_S,
        MAIL_PASSWORD=MAIL_PASSWORD_S,
        MAIL_FROM=email,
        MAIL_PORT=MAIL_PORT_S,
        MAIL_SERVER=MAIL_SERVER_S,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True
    )   
    html = open("email.html","r")
    template = html.read().format(
        user=username,
        end_point_verify=code_validation)
    message = MessageSchema(
        subject="Mail de confirmación pyRobots",
        recipients=[email],
        body=template,
        subtype='html',
    ) 
    fm = FastMail(conf)
    await fm.send_message(message)

