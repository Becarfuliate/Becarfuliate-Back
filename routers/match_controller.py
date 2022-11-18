from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from schemas import imatch
from crud import match_service, websocket_services
from routers.simulation_controller import game
from crud import simulation_service as sc
from crud.robot_service import get_file_by_id
from random import randint

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


@match_end_points.post("/match/run")
async def start_match(id_match: int, name_user: str):
    robot_list = match_service.start_game(id_match, name_user)
    if "Status" in robot_list:
        return robot_list
    n_rounds = match_service.get_match_rounds(id_match)
    n_games = match_service.get_match_games(id_match)

    robots = match_service.parse_robots(robot_list)
    outer_response = match_service.add_robot_attributes(
        n_games, n_rounds, robots, robot_list
    )
    juego = match_service.games_last_round(outer_response)
    resultado = match_service.get_winners(juego)

    return resultado


@match_end_points.websocket("/ws/match/{id_game}/{tkn}/{id_robot}")
async def join_match(websocket: WebSocket, id_game: int, tkn: str, id_robot: int):
    await manager.connect(websocket, id_game, tkn, id_robot)


@match_end_points.get("/matchs")
async def read_matchs(token: str):
    msg = match_service.read_matchs(token)
    return msg
