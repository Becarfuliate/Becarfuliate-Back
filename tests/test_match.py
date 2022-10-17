from random import randint
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

# Test sobre /match/add


def test_match_add_success():
    """
    TEST_0: Agregar partida correctamente.
        PRE: Que la partida no haya sido creada.
    """
    response = client.post(
        "/login",
        json={
            "username": "Alexis",
            "email": "ale@gmail.com",
            "password": "Asd23asdasdasdasd@",
        },
    )
    toq_var = response.json()["token"]
    num_partida = randint(0, 200)
    nombre_partida = "NombrePartida" + str(num_partida)
    response = client.post(
        "/match/add",
        json={
            "name": nombre_partida,
            "max_players": 4,
            "min_players": 2,
            "password": "Asd23asdasdasdasd@",
            "n_matchs": 2,
            "n_rounds_matchs": 2,
            "user_creator": "Alexis",
            "token": toq_var,
        },
    )
    assert response.json() == {"Status": "Match added succesfully"}


def test_match_add_bad_max_players():
    """
    TEST_1: Agregar partida incorrectamente, sobrepasando el número máximo de jugadores
            devuelve un error de 422.
    """
    response = client.post(
        "/login",
        json={
            "username": "Alexis",
            "email": "ale@gmail.com",
            "password": "Asd23asdasdasdasd@",
        },
    )
    toq_var = response.json()["token"]
    response = client.post(
        "/match/add",
        json={
            "name": "XKCD",
            "max_players": 5,
            "min_players": 2,
            "password": "Asd23asdasdasdasd@",
            "n_matchs": 4,
            "n_rounds_matchs": 4,
            "user_creator": "Alexis",
            "token": toq_var,
        },
    )
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "max_players"],
                "msg": "El valor debe estar entre 2 y 4",
                "type": "value_error",
            }
        ]
    }


def test_match_add_bad_min_players():
    """
    TEST_2: Agregar partida incorrectamente, sobrepasando el número min de jugadores
            devuelve un error de 422.
    """
    response = client.post(
        "/login",
        json={
            "username": "Alexis",
            "email": "ale@gmail.com",
            "password": "Asd23asdasdasdasd@",
        },
    )
    toq_var = response.json()["token"]
    response = client.post(
        "/match/add",
        json={
            "name": "XKCD",
            "max_players": 4,
            "min_players": 1,
            "password": "Asd23asdasdasdasd@",
            "n_matchs": 4,
            "n_rounds_matchs": 4,
            "user_creator": "Alexis",
            "token": toq_var,
        },
    )
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "min_players"],
                "msg": "El valor debe estar entre 2 y 4",
                "type": "value_error",
            }
        ]
    }


def test_match_add_bad_number_matchs():
    """
    TEST_3: Agregar partida incorrectamente, sobrepasando el número de juegos
            devuelve un error de 422.
    """
    response = client.post(
        "/login",
        json={
            "username": "Alexis",
            "email": "ale@gmail.com",
            "password": "Asd23asdasdasdasd@",
        },
    )
    toq_var = response.json()["token"]
    response = client.post(
        "/match/add",
        json={
            "name": "XKCD",
            "max_players": 4,
            "min_players": 2,
            "password": "Asd23asdasdasdasd@",
            "n_matchs": 201,
            "n_rounds_matchs": 4,
            "user_creator": "Alexis",
            "token": toq_var,
        },
    )
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "n_matchs"],
                "msg": "El valor debe estar entre 1 y 200",
                "type": "value_error",
            }
        ]
    }


def test_match_add_bad_number_rounds():
    """
    TEST_4: Agregar partida incorrectamente, sobrepasando el número de rondas
            devuelve un error de 422.
    """
    response = client.post(
        "/login",
        json={
            "username": "Alexis",
            "email": "ale@gmail.com",
            "password": "Asd23asdasdasdasd@",
        },
    )
    toq_var = response.json()["token"]
    response = client.post(
        "/match/add",
        json={
            "name": "XKCD",
            "max_players": 4,
            "min_players": 2,
            "password": "Asd23asdasdasdasd@",
            "n_matchs": 200,
            "n_rounds_matchs": 10001,
            "user_creator": "Alexis",
            "token": toq_var,
        },
    )
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "n_rounds_matchs"],
                "msg": "El valor debe estar entre 2 y 10.000",
                "type": "value_error",
            }
        ]
    }


def test_match_add_bad_name():
    """
    TEST_5: Agregar partida incorrectamente, colocando un nombre vacío
            devuelve un error de 422.
    """
    response = client.post(
        "/login",
        json={
            "username": "Alexis",
            "email": "ale@gmail.com",
            "password": "Asd23asdasdasdasd@",
        },
    )
    toq_var = response.json()["token"]
    response = client.post(
        "/match/add",
        json={
            "name": " ",
            "max_players": 4,
            "min_players": 2,
            "password": "Asd23asdasdasdasd@",
            "n_matchs": 200,
            "n_rounds_matchs": 10000,
            "user_creator": "Alexis",
            "token": toq_var,
        },
    )
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "msg": "El nombre no puede contener caracteres vacíos",
                "type": "value_error",
            }
        ]
    }


def test_match_add_bad_name_long():
    """
    TEST_6: Agregar partida incorrectamente, colocando un nombre vacío
            devuelve un error de 422.
    """
    response = client.post(
        "/login",
        json={
            "username": "Alexis",
            "email": "ale@gmail.com",
            "password": "Asd23asdasdasdasd@",
        },
    )
    toq_var = response.json()["token"]
    response = client.post(
        "/match/add",
        json={
            "name": "        ",
            "max_players": 4,
            "min_players": 2,
            "password": "Asd23asdasdasdasd@",
            "n_matchs": 200,
            "n_rounds_matchs": 10000,
            "user_creator": "Alexis",
            "token": toq_var,
        },
    )
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "msg": "El nombre no puede contener caracteres vacíos",
                "type": "value_error",
            }
        ]
    }


def test_match_add_bad_name_long_v1():
    """
    TEST_7: Agregar partida incorrectamente, colocando un nombre (caracter + vacío)
            devuelve un error de 422.
    """
    response = client.post(
        "/login",
        json={
            "username": "Alexis",
            "email": "ale@gmail.com",
            "password": "Asd23asdasdasdasd@",
        },
    )
    toq_var = response.json()["token"]
    response = client.post(
        "/match/add",
        json={
            "name": "s        ",
            "max_players": 4,
            "min_players": 2,
            "password": "Asd23asdasdasdasd@",
            "n_matchs": 200,
            "n_rounds_matchs": 10000,
            "user_creator": "Alexis",
            "token": toq_var,
        },
    )
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "msg": "El nombre no puede contener caracteres vacíos",
                "type": "value_error",
            }
        ]
    }


def test_match_add_bad_name_long_v2():
    """
    TEST_8: Agregar partida incorrectamente, colocando un nombre (vacío + caracter)
            devuelve un error de 422.
    """
    response = client.post(
        "/login",
        json={
            "username": "Alexis",
            "email": "ale@gmail.com",
            "password": "Asd23asdasdasdasd@",
        },
    )
    toq_var = response.json()["token"]
    response = client.post(
        "/match/add",
        json={
            "name": "         s",
            "max_players": 4,
            "min_players": 2,
            "password": "Asd23asdasdasdasd@",
            "n_matchs": 200,
            "n_rounds_matchs": 10000,
            "user_creator": "Alexis",
            "token": toq_var,
        },
    )
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "msg": "El nombre no puede contener caracteres vacíos",
                "type": "value_error",
            }
        ]
    }


def test_match_add_bad_type_insert_v0():
    """
    TEST_9: Agregar partida incorrectamente, un caracter en campos numéricos.
            devuelve un error de 422.
    """
    response = client.post(
        "/login",
        json={
            "username": "Alexis",
            "email": "ale@gmail.com",
            "password": "Asd23asdasdasdasd@",
        },
    )
    toq_var = response.json()["token"]
    response = client.post(
        "/match/add",
        json={
            "name": "XKCD",
            "max_players": "s",
            "min_players": 2,
            "password": "Asd23asdasdasdasd@",
            "n_matchs": 200,
            "n_rounds_matchs": 10000,
            "user_creator": "Alexis",
            "token": toq_var,
        },
    )
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "max_players"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
    }


# Comentado pues aún no validé el input del token.
# def test_match_add_bad_type_insert_v1():
#     """
#     TEST_10: Agregar partida incorrectamente, un caracter en campos numéricos.
#             devuelve un error de 422.
#     """
#     response = client.post(
#         "/match/add",
#         json={
#             "name": "XKCD",
#             "max_players": 4,
#             "min_players": 2,
#             "password": "Asd23asdasdasdasd@",
#             "n_matchs": 200,
#             "n_rounds_matchs": 10000,
#             "user_creator": "Alexis",
#             "token": " ",
#         },
#     )
#     assert response.json() == {"detail": "El campo ingresado no es numérico"}


# {
#   "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiJBbGV4aXMiLCJleHBpcnkiOiIyMDIyLTEwLTE4IDE3OjI2OjMzLjIxNzk3OCJ9.csgJCbGK40SofBwrMYhCNHHkSCl7RIflINlpwFeDXAE"
# }
