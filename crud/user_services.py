from models.entities import User
from pony.orm import db_session, commit
from schemas.iuser import User_create
from cryptography.fernet import Fernet
import jwt
from datetime import datetime, timedelta
from decouple import config
import random


# se obtienen de env
JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")
JWT_EXPIRES = timedelta(1)
KEY_CRYPT = config("KEY")


@db_session()
def add_user(new_user: User_create):
    '''
    Agrega un usuario a la base de datos, devolviendo un
    mensaje representativo del estado de la salida
    Args:
        new_user: Usuario a persistir

    Returns:
        String representativa del estado de la salida
    '''
    password_encrypted = encrypt_password(new_user.password)
    # Generamos un codigo de privacidad para la verificacion de mail
    code_for_validation = ''.join(
        random.sample(password_encrypted[7:13], 6)
        )
    with db_session:
        try:
            User(
                username=new_user.username,
                password=password_encrypted,
                confirmation_mail=False,
                email=new_user.email,
                validation_code=code_for_validation
            )
            commit()
        except Exception as e:
            return str(e)
        return "Usuario agregado con exito"


@db_session
def update_confirmation(username: str, code: str):
    """
    Actualiza el valor del atributo que representa que
    el la cuenta fue confirmada
    Args:
        username: Usuario confirmado
        code: Codigo de privacidad para la validacion
    Returns:
        String representativa del estado de la salida
    """
    try:
        user_for_validate = User[username]
    except Exception as e:
        return str(e)+" no existe"
    if (code == user_for_validate.validation_code):
        user_for_validate.confirmation_mail = True
        return "Usuario confirmado con exito"
    return "El codigo de confirmacion no es valido"


@db_session
def get_code_for_user(username: str):
    """
    Trae el codigo de privacidad de la validacion
    de la base de datos
    Args:
        username: Usuario del cual queremos el codigo
    Returns:
        Error: String representativa del estado de la salida
        Exito: Codigo de privacidad
    """
    try:
        code = User[username].validation_code
    except Exception as e:
        return str(e)+" no existe"
    return code


# busca un usuario en la base de datos por su nombre
@db_session()
def search_user(name):
    data = User.get(username=name)
    return data


@db_session
def search_user_by_email(input_email):
    data = User.select(lambda p: p.email == input_email).get()
    return data


# FUNCIONES AUXILIARES

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


# esta funcion desencripta una password
def decrypt_password(password: str):
    f = Fernet(KEY_CRYPT)
    encoded_pasword = password.encode()
    decripted_password = f.decrypt(encoded_pasword)
    decoded_password = decripted_password.decode()
    return decoded_password


def encrypt_password(password: str):
    """
    Realiza un encriptado simetrico a un string
    haciendo uso de Fernet
    Args:
        password: String a encriptar
    Returns:
        String encriptada
    """
    f = Fernet(KEY_CRYPT)
    encoded_pasword = password.encode()
    encripted_password = f.encrypt(encoded_pasword)
    decoded_password = encripted_password.decode()
    return decoded_password
