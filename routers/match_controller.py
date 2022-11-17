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
    outer_response = []
    robots = []
    for x in robot_list:
        file = get_file_by_id(x)
        if "default1" in file:
            file = "default1.py"
        elif "default2" in file:
            file = "default2.py"

        filename = "routers/robots/" + file
        exec(
            open(filename).read(),
            globals(),
        )
        file = file.strip(".py")
        file = file.split("_")[0]
        klass = globals()[file]
        r = klass((randint(100, 800), randint(100, 800)), randint(0, 360))
        robots.append(r)

    for i in range(n_games):
        outer_response.append(game(robots, n_rounds))
        for j in outer_response:
            for i in j:
                k = 0
                for j in i:
                    j["id"] = robot_list[k]
                    j["nombre"] = sc.get_robot_name(robot_list[k])
                    j["imagen"] = sc.get_robot_avatar(robot_list[k])
                    k += 1
    return outer_response


@match_end_points.websocket("/ws/match/{id_game}/{tkn}/{id_robot}")
async def join_match(websocket: WebSocket, id_game: int, tkn: str, id_robot: int):
    await manager.connect(websocket, id_game, tkn, id_robot)


@match_end_points.get("/matchs")
async def read_matchs(token: str):
    msg = match_service.read_matchs(token)
    return msg
