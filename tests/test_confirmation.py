from crud.user_services import get_code_for_user
import pytest
from fastapi.testclient import TestClient
import main


client = TestClient(main.app)


def client_get_verify(username_to_ver, user_code):
    return client.get(
        url="http://localhost:8000/verify?"
        "username="+username_to_ver+"&code="+user_code
    )


def test_confirmation_success():
    response = client_get_verify(
        username_to_ver="anonymous",
        user_code=get_code_for_user("anonymous")
        )
    assert response.json()["Status"] == "Usuario confirmado con exito"


def test_confirmation_user_wrong():
    user_wrong = "anonymousNotExist"
    response = client_get_verify(
        username_to_ver=user_wrong,
        user_code=get_code_for_user("anonymous")
        )
    assert response.json()["detail"] == "El usuario "+user_wrong+" no existe"


def test_confirmation_code_wrong():
    response = client_get_verify(
        username_to_ver="anonymous",
        user_code="elToken"
        )
    assert response.json()["detail"] == "El codigo de confirmacion"
    "no es valido"
