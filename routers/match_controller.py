from fastapi import APIRouter, HTTPException
from schemas import imatch
from crud import match_service

match_end_points = APIRouter()


@match_end_points.post("/match/add")
async def create_match(match: imatch.MatchCreate):
    msg = match_service.create_match(match)
    if "IntegrityError" in msg and "name" in msg:
        raise HTTPException(status_code=409, detail="El nombre de la partida ya existe")
    if "ObjectNotFound" in msg:
        raise HTTPException(status_code=400, detail="El usuario o email no existe")
    return {"Status": "Match added succesfully"}


@match_end_points.get("/matchs")
async def read_matchs(token: str):
    msg = match_service.read_matchs(token)
    return msg


# Funcion para listar una partida por id
# @match_end_points.get("/match/{id_match}")
# async def read_match(id_match: int):
#     result = match_service.read_match(abs(id_match))
#     if "Match" in result:
#         raise HTTPException(status_code=409, detail="La partida no existe")
#     return result
