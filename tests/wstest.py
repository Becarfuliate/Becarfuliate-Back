from routers.match_controller import match_end_points
from fastapi.testclient import TestClient
from pony.orm import db_session

# "match/join?id_match=" + str(id_match) + "&name_user=" + "Capogrossi"


# def test_websocket():
#     client = TestClient(match_end_points)
#     with client.websocket_connect("/ws/match/join/5/lichi") as websocket:
#         data = websocket.receive_json()
#         assert data == {'msg': 'lichi has joined the game'}
#     with client.websocket_connect("/ws/match/join/5/agus") as websocket2:
#         data = websocket2.receive_json()
#         data2 = websocket.receive_json()
#         assert data == {'msg': 'agus has joined the game'}
#         assert data2 == {'msg': 'agus has joined the game'}
#     with client.websocket_connect("/ws/match/join/2/jesus") as websocket3:
#         data3 = websocket3.receive_json()
#         assert data3 == {'msg': 'jesus has joined the game'}

# Preparando la BD para el test
def client_post_register(username, password, email):
    return client.post(
        "/register",
        json={
            "username": username,
            "password": password,
            "email": email
            }
    )

@db_session
def elim_user(username: str):
    with db_session:
        User[username].delete()


def delete_db():
    elim_user("anonymous")

def load_bd():
    client_post_register(
        "anonymous",
        "Asd23asdasdasdasd@",
        "anonymous@hotmail.com"
    )

# Test en si
def test_websocket():
    client = TestClient(match_end_points)
    with client.websocket_connect("/ws/match/2/Lichi/1") as websocket:
        data = websocket.receive_json()
        assert data == {'msg': 'Lichi has joined the game'}