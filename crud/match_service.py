from datetime import datetime

# from types import NoneType
from pony.orm import db_session, commit, select, left_join
from schemas import imatch
from models.entities import Match, User, Robot
from crud.user_services import decode_JWT, encrypt_password, search_user_by_email
from routers.simulation_controller import game
from crud import simulation_service as sc
from crud.robot_service import get_file_by_id
from random import randint
import re


def is_email(user_crator: str):
    regex = (
        r"[a-zA-Z0-9_.-]+[^!#$%^&*()]@(?:gmail"
        r"|hotmail|yahoo|live|mi.unc|outlook)\.(?:com|es|edu.ar)"
    )
    result = isinstance(re.search(regex, user_crator), re.Match)
    return result


def is_username(user_creator: str):
    result = True
    if user_creator == "":
        resutl = False
    if " " in user_creator:
        result = False
    if len(user_creator) > 40:
        result = False
    return result


def find_by_username_or_email(user_creator: str):
    if is_email(user_creator):
        result = search_user_by_email(user_creator)
        if isinstance(result, NoneType):
            raise Exception
    elif is_username(user_creator):
        result = User[user_creator]
    return result


@db_session
def create_match(match: imatch.MatchCreate):
    with db_session:
        decode_token = decode_JWT(match.token)
        if decode_token["expiry"] > str(datetime.now()):
            try:
                creator_aux = find_by_username_or_email(match.user_creator)
            except Exception as e:
                return "ObjectNotFound"
            try:
                Match(
                    name=match.name,
                    max_players=abs(match.max_players),
                    min_players=abs(match.min_players),
                    password=encrypt_password(match.password),
                    n_matchs=min(abs(match.n_matchs), 200),
                    n_rounds_matchs=min(abs(match.n_rounds_matchs), 10000),
                    users={
                        creator_aux,
                    },
                    user_creator=creator_aux,
                )
                commit()
            except Exception as e:
                return str(e)
        else:
            return "Token no válido"
        return "added"


@db_session
def read_matchs(token: str):
    with db_session:
        decode_token = decode_JWT(token)
        if decode_token["expiry"] > str(datetime.now()):
            try:
                matchs = Match.select()
                result = [imatch.Match.from_orm(p) for p in matchs]
                commit()
            except Exception as e:
                return str(e)
        else:
            result = "Token no válido"
        return result


@db_session
def read_match(id_match: int):
    with db_session:
        try:
            match = Match[id_match]
            result = imatch.Match.from_orm(match)
            commit()
        except Exception as e:
            return str(e)
        return result


@db_session
def get_match_id(match_name: str):
    result = select(m.id for m in Match if m.name == match_name)
    for i in result:
        return i


@db_session
def get_match_rounds(match_id: int):
    query = select(m.n_rounds_matchs for m in Match if m.id == match_id)
    for i in query:
        result = i
    return result


@db_session
def get_match_games(match_id: int):
    query = select(m.n_matchs for m in Match if m.id == match_id)
    for i in query:
        result = i
    return result


@db_session
def read_match_players(id_match: int):
    result = select(m.users for m in Match if m.id == id_match)
    return result


@db_session
def read_player_in_game(username: str, id_match: int):
    result = select(m.users for m in Match if m.id == id_match)

    return username in result


@db_session
def add_player(id_match: int, tkn: str, id_robot: int):
    result = ""
    with db_session:
        decode_token = decode_JWT(tkn)
        error = ""
        username = decode_token["userID"]
        if str(decode_token["expiry"]) < str(datetime.now()):
            return "Token no valido"
        try:
            match = Match[id_match]
            user = User[username]
            robot = Robot[id_robot]
            if len(match.users) == match.max_players:
                error = "La partida esta llena"
            elif str(robot.name).split("_")[1] != username:
                error = "El robot no pertenece al usuario"
            elif user in match.users:
                error = "El usuario ya esta en la partida"
        except Exception as e:
            if "Match" in str(e):
                error = "La partida no existe"
            elif "User" in str(e):
                error = "El usuario no existe"
            elif "Robot" in str(e):
                error = "El robot no existe"
            return error
        if error == "":
            match.users.add(user)
            list_robots = match.robots_in_match
            list_robots.append(id_robot)
            match.robots_in_match = list_robots
            result = str(username) + ":" + str(robot.name).split("_")[0]
        else:
            result = error
    return result


@db_session
def remove_player(id_match: int, name_user: str):
    try:
        result = ""
        match = Match[id_match]
        user = User[name_user]
        for i in match.users:
            if user.username not in i.username:
                result = "El usuario no está en la partida"
            else:
                result = "El usuario fue removido de la partida"
        match.users.remove(user)
    except Exception as e:
        error = ""
        if "Match" in str(e):
            error = "La partida no existe"
        elif "User" in str(e):
            error = "El usuario no existe"
        return error
    return result


@db_session
def start_game(id_match: int, name_user: str):
    try:
        msg = ""
        match = Match[id_match]
        user = User[name_user]
        if not user.username == match.user_creator.username:
            msg = {"Status": "No es el creador de la partida"}
            return msg
        match_robots = match.robots_in_match
        if len(match_robots) < 2:
            msg = {"Status": "La partida no tiene suficientes jugadores"}
            return msg
    except Exception as e:
        return str(e)
    return list(match_robots)


def parse_robots(robot_list: list):
    robots = []
    for x in robot_list:
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
    return robots


def add_robot_attributes(
    n_games: int, n_rounds: int, robots: list, robot_id_list: list
):
    outer_response = []
    for i in range(n_games):
        outer_response.append(game(robots, n_rounds))
        for j in outer_response:
            for i in j:
                k = 0
                for j in i:
                    j["id"] = robot_id_list[k]
                    j["nombre"] = sc.get_robot_name(robot_id_list[k])
                    j["imagen"] = sc.get_robot_avatar(robot_id_list[k])
                    k += 1
    return outer_response


def games_last_round(outer_response: list):
    final_round = []
    juego = {}
    contador = 0
    # Para cada partida
    for i in outer_response:
        contador += 1
        # Para rondas de partida
        for j in i:
            final_round.append(j)
        juego["Juego: " + str(contador)] = final_round[-1]
    return juego


def get_winners(juego: list):
    robots_sobrevivientes = []
    resultado = {}
    contador2 = 0
    for i in juego:
        contador2 += 1
        for j in juego[i]:
            if j["vida"] > 0:
                robots_sobrevivientes.append(j)
        resultado["Ganador/es juego: " + str(contador2)] = robots_sobrevivientes
        robots_sobrevivientes = []
    return resultado
