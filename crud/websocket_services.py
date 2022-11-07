from typing import Dict
from fastapi import WebSocket


class ConnectionManager:
    """
    Handler of socket connections
    """

    def __init__(self):
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, id_game: int, id_player: int):
        await websocket.accept()
        if id_game in self.active_connections:  # Exist game in active_connections
            self.active_connections[id_game].update({id_player: websocket})
        else:
            self.active_connections[id_game] = {id_player: websocket}

    async def disconnect(self, id_game: int, id_player: int):
        await self.active_connections[id_game].get(id_player).close()
        self.active_connections[id_game].pop(id_player)
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

    def exist_socket_of_player(self, id_game: int, id_player: int) -> bool:
        game = self.active_connections.get(id_game)
        if game != None:
            return True
        return False

    def get_all_connections(self):
        return self.active_connections

    def get_socket_player(self, id_game: int, id_player: int) -> WebSocket:
        game = self.active_connections.get(id_game)
        if game != None:
            player = id_player
            return id_player
