from datetime import datetime
from pony.orm import db_session, commit,select
from models.entities import Robot, User
from crud.user_services import decode_JWT
from fastapi import UploadFile
from schemas import irobot

def validate_file(
    filename: str,
    file: UploadFile
):
    """Validación de un archivo, i.e chequea extención '.py' y que el nombre del archivo sea usado dentro.

    Args:
        filename (str): Nombre de archivo a validar
        file (UploadFile): Archivo a validar

    Returns:
        bool: True en caso de que sea válido.
    """
    content = file.file.read().decode()
    is_valid = True
    if (filename+".py" != file.filename):
        is_valid = False
    if not (filename in content):
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
    """Agregar robot a la base de datos.

    Args:
        config_file (UploadFile): Archivo '.py' del robot.
        avatar_file (str): Imagen del robot.
        robot_name (str): Nombre del robot.
        user_token (str): Token.
        username (str): Nombre de usuario o email.

    Returns:
        str: Mensaje de retorno.
    """
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
                    name=robot_name+"_"+user_for_validate.username,
                    avatar=avatar_file+"_"+user_for_validate.username,
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
    """Listar robots, consulta a la base de datos.

    Args:
        token (str): token.

    Returns:
        str: En caso de error.
        List[Robot]: Lista de robots.
    """
    with db_session:
        decode_token = decode_JWT(token)
        result = []
        if decode_token["expiry"] > str(datetime.now()):
            try:
                user = decode_token["userID"]
                robots = select(x for x in Robot if x.user_owner.username == user)
                result = [irobot.Robot.from_orm(r) for r in robots]
                commit()
            except Exception as e:
                return str(e)
        else:
            result = "Token no válido"
        return result

@db_session
def get_file_by_id(rob_id: int):
    """Obtener un archivo por su id

    Args:
        rob_id (int): id del archivo

    Returns:
        Any: Nombre del archivo del robot.
    """
    with db_session:
        robot = Robot[rob_id]
        filename = robot.name+".py"
        return filename

@db_session
def add_default_robot(username:str):
    """Agregar robot por defecto.

    Args:
        username (str): Usuario al que agregar robot por defecto.
    """
    with db_session:
        Robot(
                    name="default1"+"_"+username,
                    matchs_pleyed=0,
                    matchs_won=0,
                    avg_life_time=0,
                    user_owner=username
                )
        commit()
        Robot(
                    name="default2"+"_"+username,
                    matchs_pleyed=0,
                    matchs_won=0,
                    avg_life_time=0,
                    user_owner=username
                )
        commit()
        