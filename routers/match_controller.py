from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from schemas import imatch
from crud import match_service, websocket_services

match_end_points = APIRouter()

manager = websocket_services.ConnectionManager()


@match_end_points.post("/match/add")
async def create_match(match: imatch.MatchCreate):
    msg = match_service.create_match(match)
    if "IntegrityError" in msg and "name" in msg:
        raise HTTPException(status_code=409, detail="El nombre de la partida ya existe")
    if "ObjectNotFound" in msg:
        raise HTTPException(status_code=400, detail="El usuario o email no existe")
    return {"Status": "Match added succesfully"}


@match_end_points.websocket("/ws/match/{id_game}/{tkn}/{id_robot}")
async def join_match(websocket: WebSocket, id_game: int, tkn: str, id_robot: int):
    await manager.connect(websocket, id_game, tkn, id_robot)


@match_end_points.get("/matchs")
async def read_matchs(token: str):
    msg = match_service.read_matchs(token)
    return msg
