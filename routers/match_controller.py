import json
from fastapi import APIRouter, HTTPException
from crud import match_service


match_end_points = APIRouter()


@match_end_points.get("/matchs")
async def read_matchs():
    result = match_service.read_matchs()
    return result


@match_end_points.get("/match/{id_match}")
async def read_match(id_match: int):
    result = match_service.read_match(abs(id_match))
    if "Match" in result:
        raise HTTPException(status_code=409, detail="La partida no existe")
    return result
