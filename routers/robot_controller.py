from fastapi import APIRouter, HTTPException, File, UploadFile, Response
from crud import robot_service
from crud.robot_service import add_robot
from pathlib import Path
import shutil
robot_end_points = APIRouter()


def store_config(file: UploadFile, owner: str):
    file.file.seek(0)
    new_filename=file.filename.replace(".py","_"+owner+".py")
    with open('routers/robots/'+new_filename, 'wb+') as upload_folder:
        shutil.copyfileobj(file.file, upload_folder)


def store_avatar(file: UploadFile, owner: str):
    file.file.seek(0)
    new_filename=file.filename.replace(".jpeg","_"+owner+".jpeg")
    new_filename=file.filename.replace(".peg","_"+owner+".peg")
    new_filename=file.filename.replace(".jpg","_"+owner+".jpg")
    with open('routers/robots/avatars/'+new_filename, 'wb+') as upload_folder:
        shutil.copyfileobj(file.file, upload_folder)


@robot_end_points.post("/upload/robot")
async def robot_upload(
    config: UploadFile,
    avatar: UploadFile,
    name: str,
    tkn: str,
    username: str
):
    """Cargar Robot

    Args:
        config (UploadFile): archivo del robot.
        avatar (UploadFile): imagen del robot.
        name (str): nombre del robot.
        tkn (str): token.
        username (str): nombre de usuario.

    Raises:
        HTTPException: 409: El robot ya existe.
        HTTPException: 400: El usuario no existe.
        HTTPException: 422: El nombre del Robot con el archivo no se corresponden.
        HTTPException: 440: El token no es correcto o está expirado.

    Returns:
        _type_: _description_
    """
    msg = add_robot(config, avatar.filename, name, tkn, username)
    # El robot ya existe
    if ("ya existe" in msg):
        raise HTTPException(
            status_code=409,
            detail=msg
            )
    # El usuario no existe
    if "no existe" in msg:
        raise HTTPException(
            status_code=400,
            detail="El usuario "+username+" no existe"
            )
    # Los nombres para el robot no se corresponden
    if "requisitos" in msg:
        raise HTTPException(
            status_code=422,
            detail=msg
            )
    # Token invalido o expirado
    if "Token" in msg:
        raise HTTPException(
            status_code=440,
            detail="Sesión expirada"
            )
    store_config(config, username)
    store_avatar(avatar, username)
    return {
        "msg": msg
    }

@robot_end_points.get("/robots")
def read_robots(token: str):
    """Listar Robots

    Args:
        token (str): token

    Returns:
        str: Error
        List[Robots]: Lista de robots.
    """
    msg = robot_service.read_robots(token)
    return msg

@robot_end_points.get("/image",responses = {200: {"content": {"image/png": {}}}}, response_class=Response)
def get_image():
    image_bytes: bytes = generate_cat_picture()
    # media_type here sets the media type of the actual response sent to the client.
    return Response(content=image_bytes, media_type="image/png")