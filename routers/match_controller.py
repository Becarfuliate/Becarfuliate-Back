from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from schemas import imatch
from crud import match_service, websocket_services

match_end_points = APIRouter()

manager = websocket_services.ConnectionManager()

# ----

from typing import Union

from fastapi import Cookie, Depends, FastAPI, Query, WebSocket, status
from fastapi.responses import HTMLResponse

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button onclick="connect(event)">Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
            function connect(event) {
                var itemId = document.getElementById("itemId")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://localhost:8000/items/" + itemId.value + "/ws?token=" + token.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@match_end_points.get("/")
async def get():
    return HTMLResponse(html)


async def get_cookie_or_token(
    websocket: WebSocket,
    session: Union[str, None] = Cookie(default=None),
    token: Union[str, None] = Query(default=None),
):
    if session is None and token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@match_end_points.websocket("/items/{item_id}/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    item_id: str,
    q: Union[int, None] = None,
    cookie_or_token: str = Depends(get_cookie_or_token),
):
    connections = await manager.connect(websocket, item_id, cookie_or_token)
    print(connections)
    while True:
        data = await connections["1"]["some-key-token"].receive_text()
        print(data)
    # while True:
    #     data = await websocket["foo"].receive_text()
    #     await manager.send_personal_json(
    #         {f"Session cookie or query token value is: {cookie_or_token}"},
    #     )
    #     if q is not None:
    #         await manager.send_text(f"Query parameter q is: {q}")
    #     await manager.send_text(f"Message text was: {data}, for item ID: {item_id}")


# ----


@match_end_points.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


@match_end_points.post("/match/add")
async def create_match(match: imatch.MatchCreate):
    msg = match_service.create_match(match)
    if "IntegrityError" in msg and "name" in msg:
        raise HTTPException(status_code=409, detail="El nombre de la partida ya existe")
    if "ObjectNotFound" in msg:
        raise HTTPException(status_code=400, detail="El usuario o email no existe")
    return {"Status": "Match added succesfully"}


@match_end_points.post("/match/join")
async def join_match(id_match: int, name_user: str):
    msg = match_service.add_player(id_match, name_user)
    return {"Status": msg}


@match_end_points.delete("/match/leave")
async def join_match(id_match: int, name_user: str):
    msg = match_service.remove_player(id_match, name_user)
    return {"Status": msg}


@match_end_points.get("/matchs")
async def read_matchs(token: str):
    msg = match_service.read_matchs(token)
    return msg
