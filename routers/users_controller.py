from fastapi import APIRouter, HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from decouple import config
from crud.user_services import (
    add_user,
    update_confirmation,
    get_code_for_user,
    search_user_by_email,
    search_user,
    sign_JWT,
    decrypt_password,
)
from schemas.iuser import User_base, User_login_schema

user_end_points = APIRouter()


@user_end_points.post("/login")
async def user_login(credentials: User_login_schema):
    if credentials.username == "":
        data = search_user_by_email(credentials.email)
    else:
        data = search_user(credentials.username)

    if data is None:
        raise HTTPException(status_code=400, detail="No existe el usuario")
    else:
        pass_decrypt = decrypt_password(data.password)
        mail_is_verificated = data.confirmation_mail
        password_is_correct = credentials.password == pass_decrypt

        if not mail_is_verificated:
            raise HTTPException(status_code=400, detail="Email no verificado")
        elif not password_is_correct:
            raise HTTPException(
                status_code=400,
                detail="Contraseña incorrecta"
                )
        else:
            response = sign_JWT(credentials.username)
            return {"token": response}


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
    if "no existe" in code_validation:
        raise HTTPException(
            status_code=400,
            detail="El usuario "+user_to_add.username+" no existe"
            )
    await send_confirmation_mail(
        user_to_add.email,
        code_validation,
        user_to_add.username
        )
    return {"Status": msg}


@user_end_points.get("/verify")
def user_verification(username: str, code: str):
    msg = update_confirmation(username, code)
    if "no existe" in msg:
        raise HTTPException(
            status_code=400,
            detail="El usuario "+username+" no existe"
            )
    if msg == "El codigo de confirmacion no es valido":
        raise HTTPException(
            status_code=400,
            detail=msg
            )
    return {"Status": msg}


MAIL_USERNAME_S = config("MAIL_USERNAME")
MAIL_PASSWORD_S = config("MAIL_PASSWORD")
MAIL_PORT_S = config("MAIL_PORT")
MAIL_SERVER_S = config("MAIL_SERVER")


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
        USE_CREDENTIALS=True,
    )
    html = open("email.html", "r")
    template = html.read().format(
        user=username,
        end_point_verify=code_validation
        )
    message = MessageSchema(
        subject="Mail de confirmación pyRobots",
        recipients=[email],
        body=template,
        subtype="html",
    )
    fm = FastMail(conf)
    await fm.send_message(message)
