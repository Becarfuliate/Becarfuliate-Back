from datetime import datetime
from distutils.command.config import config
from attr import validate
from pony.orm import db_session, commit
from schemas import irobot
from models.entities import Robot, User
from crud.user_services import decode_JWT
from fastapi import UploadFile


def validate_file(
    filename: str,
    file: UploadFile
):
    content = file.file.read().decode()
    is_valid = True
    if filename + ".py" != file.filename:
        print("fallo 1")
        is_valid = False
    if not (filename in content):
        print("fallo 2")
        is_valid = False
    return is_valid


@db_session
def add_robot(
    config_file: UploadFile,
    avatar_file: str,
    robot_name: str,
    user_token: str,
    username: str
):
    with db_session:
        decode_token = decode_JWT(user_token)
        vto = decode_token["expiry"]
        if not (str(vto) > str(datetime.now())) or (vto == 0):
            return "Token no válido"
        if validate_file(robot_name, config_file):
            try:
                user_for_validate = User[username]
            except Exception as e:
                return str(e) + " no existe"
            try:
                Robot(
                    name=robot_name + user_for_validate.username,
                    avatar=avatar_file,
                    matchs_pleyed=0,
                    matchs_won=0,
                    avg_life_time=0,
                    user_owner=user_for_validate.username
                )
                commit()
            except Exception as e:
                return str("El robot ya existe")
        else:
            return "El archivo no cumple los requisitos"
        return "Robot agregado con exito"


@db_session
def read_robots(token: str):
    with db_session:
        decode_token = decode_JWT(token)
        if decode_token["expiry"] > str(datetime.now()):
            try:
                robots = Robot.select()
                result = [irobot.Robot.from_orm(r) for r in robots]
                commit()
            except Exception as e:
                return str(e)
        else:
            result = "Token no válido"
        return result
