from fastapi import APIRouter, HTTPException
from schemas import imatch
from crud import match_service

match_end_points = APIRouter()


@match_end_points.post("/match/add")
def create_match(match: imatch.MatchCreate):
    msg = match_service.create_match(match)
    if "IntegrityError" in msg and "name" in msg:
        raise HTTPException(status_code=409, detail="El nombre de la partida ya existe")
    return {"Status": "Match added succesfully"}
