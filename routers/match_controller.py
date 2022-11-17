from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from schemas import imatch
from crud import match_service, websocket_services
from routers.simulation_controller import game
from crud import simulation_service as sc
from crud.robot_service import get_file_by_id
from routers.game.game import inflingir_danio, avanzar_ronda
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


@match_end_points.websocket("/ws/match/join/{id_game}/{user_name}")
async def join_match(websocket: WebSocket, id_game: int, user_name: str):
    msg = match_service.add_player(id_game, user_name)
    await manager.connect(websocket, id_game, user_name)
    return {"Status": msg}

    # while True:
    #     data = await connections[id_match][name_user].receive_text()
    #     print(data)


@match_end_points.post("/match/run")
async def start_match(id_match: int, name_user: str):
    msg = match_service.start_game(id_match, name_user)
    robot_list = ""
    for i in msg:
        robot_list = robot_list + i.username + ","
    robot_list = "1,2"
    n_rounds = match_service.get_match_rounds(id_match)
    n_games = match_service.get_match_games(id_match)
    parsed_robot_list = robot_list.split(",")
    outer_response = []
    robots = []
    for x in parsed_robot_list:
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
                    j["id"] = parsed_robot_list[k]
                    j["nombre"] = sc.get_robot_name(parsed_robot_list[k])
                    k += 1
    return outer_response


@match_end_points.delete("/match/leave")
async def leave_match(id_match: int, name_user: str):
    msg = match_service.remove_player(id_match, name_user)
    return {"Status": msg}


@match_end_points.get("/matchs")
async def read_matchs(token: str):
    msg = match_service.read_matchs(token)
    return msg
