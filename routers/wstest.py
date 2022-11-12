from routers.match_controller import match_end_points
from fastapi.testclient import TestClient

# "match/join?id_match=" + str(id_match) + "&name_user=" + "Capogrossi"


def test_websocket():
    client = TestClient(match_end_points)
    with client.websocket_connect("/ws/match/join/5/lichi") as websocket:
        data = websocket.receive_json()
        assert data == {"msg": "Hello WebSocket"}


def test_add2():
    client = TestClient(match_end_points)
    with client.websocket_connect("/ws/match/join/5/agus") as websocket:
        data = websocket.receive_json()
        assert data == {"msg": "Hello WebSocket"}


def test_add3():
    client = TestClient(match_end_points)
    with client.websocket_connect("/ws/match/join/3/chota") as websocket:
        data = websocket.receive_json()
        assert data == {"msg": "Hello WebSocket"}
