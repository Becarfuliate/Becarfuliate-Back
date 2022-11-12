from typing import Dict
from fastapi import WebSocket


class ConnectionManager:
    """
    Handler of socket connections
    """

    def __init__(self):
        self.active_connections: Dict[int, Dict[str, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, id_game: int, user_name: str):
        await websocket.accept()
        if id_game in self.active_connections:  # Exist game in active_connections
            self.active_connections[id_game].update({user_name: websocket})
            # return self.active_connections
        else:
            self.active_connections[id_game] = {user_name: websocket}
            # return self.active_connections
        await websocket.send_json({"msg": str(self.active_connections)})

    async def disconnect(self, id_game: int, name_player: int):
        await self.active_connections[id_game].get(name_player).close()
        self.active_connections[id_game].pop(name_player)
        if self.active_connections[id_game] == {}:  # Empty game
            self.active_connections.pop(id_game)

    async def send_personal_json(self, message, websocket: WebSocket):
        await websocket.send_json(message)
        return

    async def broadcast_text(self, id_game: int, message: str):
        game = self.active_connections.get(id_game)
        if game != None:
            for connection in game.values():
                await connection.send_text(message)
        return

    async def broadcast_json(self, id_game: int, message):
        game = self.active_connections.get(id_game)
        if game != None:
            for connection in game.values():
                await connection.send_json(message)
        return

    def exist_socket_of_player(self, id_game: int, name_player: int) -> bool:
        game = self.active_connections.get(id_game)
        if game != None:
            return True
        return False

    def get_all_connections(self):
        return self.active_connections

    def get_socket_player(self, id_game: int, name_player: int) -> WebSocket:
        game = self.active_connections.get(id_game)
        if game != None:
            player = name_player
            return name_player
