from random import randint
from fastapi.testclient import TestClient
import main
from crud.user_services import *
from crud.match_service import *
import pytest


client = TestClient(main.app)


# Funciones auxiliares para los test
def client_post_register(username, password, email):
    return client.post(
        "/register", json={"username": username, "password": password, "email": email}
    )


@db_session
def elim_user(username: str):
    with db_session:
        User[username].delete()


@db_session
def client_fast_confirmation(username: str):
    with db_session:
        User[username].confirmation_mail = True


def delete_db():
    elim_user("Alexis")


def delete_db_v2():
    elim_user("Capogrossi")
    elim_user("Capogrossi2")
    elim_user("Capogrossi3")
    elim_user("Capogrossi4")


# Tests de partidas
def test_match_add_success():
    """
    TEST_0: Agregar partida correctamente.
        PRE: Que la partida no haya sido creada.
    """
    client_post_register("Alexis", "Asd23asdasdasdasd@", "ale@gmail.com")
    client_fast_confirmation("Alexis")
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
    TEST_1: Agregar partida incorrectamente,
    sobrepasando el número máximo de jugadores
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
    TEST_2: Agregar partida incorrectamente,
    sobrepasando el número min de jugadores
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
    TEST_7: Agregar partida incorrectamente,
    colocando un nombre (caracter + vacío)
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
    TEST_8: Agregar partida incorrectamente,
    colocando un nombre (vacío + caracter)
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


def test_match_join():
    """
    TEST_10: Unirse a la partida.
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

    client_post_register("Capogrossi", "Asdjjkhkasd-3sd@", "capo@gmail.com")
    client_fast_confirmation("Capogrossi")

    response = client.post(
        "/login",
        json={
            "username": "Capogrossi",
            "email": "capo@gmail.com",
            "password": "Asdjjkhkasd-3sd@",
        },
    )

    id_match = get_match_id(nombre_partida)
    response = client.post(
        "match/join?id_match=" + str(id_match) + "&name_user=" + "Capogrossi"
    )

    assert response.json() == {"Status": "El usuario fue agregado a la partida"}


def test_match_join_user_in_game():
    """
    TEST_12: Unirse a la partida.
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

    response = client.post(
        "/login",
        json={
            "username": "Capogrossi",
            "email": "capo@gmail.com",
            "password": "Asdjjkhkasd3-sd@",
        },
    )

    client_post_register("Capogrossi2", "Asdjjkhkasd-3sd@2", "capo2@gmail.com")
    client_fast_confirmation("Capogrossi2")

    client_post_register("Capogrossi3", "Asdjjkhkasd-3sd@3", "capo3@gmail.com")
    client_fast_confirmation("Capogrossi3")

    client_post_register("Capogrossi4", "Asdjjkhkasd-3sd@4", "capo4@gmail.com")
    client_fast_confirmation("Capogrossi4")

    id_match = get_match_id(nombre_partida)
    response = client.post(
        "match/join?id_match=" + str(id_match) + "&name_user=" + "Capogrossi"
    )
    response = client.post(
        "match/join?id_match=" + str(id_match) + "&name_user=" + "Capogrossi2"
    )
    response = client.post(
        "match/join?id_match=" + str(id_match) + "&name_user=" + "Capogrossi3"
    )
    response = client.post(
        "match/join?id_match=" + str(id_match) + "&name_user=" + "Capogrossi4"
    )
    assert response.json() == {"Status": "La partida esta llena"}


def test_match_leave():
    """
    TEST_13: Salir de la partida.
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
    nombre_partida = "NombrePartida" + str(num_partida) + str(randint(0, 99999))
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

    id_match = get_match_id(nombre_partida)

    response = client.delete(
        "match/leave?id_match=" + str(id_match) + "&name_user=" + "Alexis"
    )

    assert response.json() == {"Status": "El usuario fue removido de la partida"}
    delete_db()
    delete_db_v2()
