from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from schemas import imatch
from crud import match_service, websocket_services

match_end_points = APIRouter()

manager = websocket_services.ConnectionManager()


manager = websocket_services.ConnectionManager()


@match_end_points.websocket("/ws/{game_id}/{player_id}/")
async def websocket_endpoint(websocket: WebSocket, game_id: str, player_id: str):
    """Accept socket connection and wait to receive data.
    When the connection is accepted, Broadcast to all players in the game match, letting them know that a new player has joined.

    Args:
        websocket (WebSocket): is the socket connection.
        game_id (str): name of game
        player_id (str): name of player
    Returns:
        Broadcast to all players in the game match, letting them know that a new player has joined. It Sends an updated list of player nicknames in the game.
        {'joinPlayerEvent' : [player1.nickname, player2.nickname, ...]}
    Example of use:
        ws://127.0.0.1:8000/ws/1/5/
    """
    await manager.connect(websocket, game_id, player_id)
    try:
        out = player_in_game(game_id, player_id)
        if out == False:
            await manager.disconnect(game_id, player_id)
            return

        listOfPlayers = get_players_nickname(game_id)
        print(listOfPlayers)
        # broadcast JoinPlayerEvent
        msg = {"joinPlayerEvent": listOfPlayers}
        await manager.broadcast_json(game_id, msg)

        while True:
            # Receive data from socket and do nothing
            data = await websocket.receive_json()

    except WebSocketDisconnect:
        await manager.disconnect(game_id, player_id)
        await manager.broadcast_text(game_id, f"Player {player_id} left the Game")


@match_end_points.post("/match/add")
async def create_match(match: imatch.MatchCreate):
    """Crear una partida.

    Args:
        match (imatch.MatchCreate): Partida a crear

    Raises:
        HTTPException: IntegrityError:409 si el nombre de la partida ya existe
        HTTPException: ObjectNotFound:400 si el usuario o email no exiten

    Returns:
        dict[str, str]: {"Status": "Match added succesfully"}
    """
    msg = match_service.create_match(match)
    if "IntegrityError" in msg and "name" in msg:
        raise HTTPException(status_code=409, detail="El nombre de la partida ya existe")
    if "ObjectNotFound" in msg:
        raise HTTPException(status_code=400, detail="El usuario o email no existe")
    return {"Status": "Match added succesfully"}


@match_end_points.post("/match/join")
async def join_match(id_match: int, name_user: str):
    """Unirse a la partida con id=id_match siendo el usuario con username=name_user.

    Args:
        id_match (int): identificador de partida a unirse.
        name_user (str): nombre de usuario para unirse a esa partida.

    Raises:
        Exception: La partida está llena, la partida no existe, el usuario no existe.

    Returns:
        dict[str, str]: {"Status": msg}
    """
    msg = match_service.add_player(id_match, name_user)
    return {"Status": msg}


@match_end_points.delete("/match/leave")
async def join_match(id_match: int, name_user: str):
    msg = match_service.remove_player(id_match, name_user)
    return {"Status": msg}


@match_end_points.get("/matchs")
async def read_matchs(token: str):
    """Lista las partidas

    Args:
        token (str): recibe el token

    Returns:
        str: Error.
        List[Match]: Lista de partidas.
    """
    msg = match_service.read_matchs(token)
    if "'>' not supported between instances of 'int' and 'str'" in msg:
        raise HTTPException(status_code=401, detail="No autorizado, debe logearse")
    return msg
