from fastapi import APIRouter, HTTPException, UploadFile
from crud import robot_service
from crud.robot_service import add_robot,get_image_name
import shutil
from fastapi.responses import FileResponse

robot_end_points = APIRouter()


def store_config(file: UploadFile, owner: str):
    file.file.seek(0)
    new_filename = file.filename.replace(".py", "_" + owner + ".py")
    with open("routers/robots/" + new_filename, "wb+") as upload_folder:
        shutil.copyfileobj(file.file, upload_folder)


def store_avatar(file: UploadFile):
    file.file.seek(0)
    with open("routers/robots/avatars/" + file.filename, "wb+") as upload_folder:
        shutil.copyfileobj(file.file, upload_folder)


@robot_end_points.post("/upload/robot")
async def robot_upload(
    config: UploadFile, avatar: UploadFile, name: str, tkn: str, username: str
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
    new_name = avatar.filename.split('.')
    new_name[0] =  username + "_" + name + '.'
    new_name = "".join(new_name)
    avatar.filename = new_name

    msg = add_robot(config, avatar.filename, name, tkn, username)
    # El robot ya existe
    if "ya existe" in msg:
        raise HTTPException(status_code=409, detail=msg)
    # El usuario no existe
    if "no existe" in msg:
        raise HTTPException(
            status_code=400, detail="El usuario " + username + " no existe"
        )
    # Los nombres para el robot no se corresponden
    if "requisitos" in msg:
        raise HTTPException(status_code=422, detail=msg)
    # Token invalido o expirado
    if "Token" in msg:
        raise HTTPException(status_code=440, detail="Sesión expirada")
    store_config(config, username)
    store_avatar(avatar)
    return {"msg": msg}


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
    if "'>' not supported between instances of 'int' and 'str'" in msg:
        raise HTTPException(status_code=401, detail="No autorizado, debe logearse")
    return msg

@robot_end_points.get("/image")
def get_image(token,robot_id):
    image_name = get_image_name(token,robot_id)
    path = "routers/robots/avatars/"+image_name
    return FileResponse(path)