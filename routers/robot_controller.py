from fastapi import APIRouter, HTTPException, File, UploadFile
from crud.robot_service import add_robot
# pip install python-multipart
robot_end_points = APIRouter()


@robot_end_points.post("/upload/robot")
def robot_upload(
    config: UploadFile,
    avatar: UploadFile,
    name: str,
    tkn: str,
    username: str
):
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
    return {
        "msg": msg
    }
