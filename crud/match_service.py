from datetime import datetime

# from types import NoneType
from pony.orm import db_session, commit, select, left_join
from schemas import imatch
from models.entities import Match, User, Robot
from crud.user_services import decode_JWT, encrypt_password, search_user_by_email
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
                Match(
                    name=match.name,
                    max_players=abs(match.max_players),
                    min_players=abs(match.min_players),
                    password=encrypt_password(match.password),
                    n_matchs=min(abs(match.n_matchs), 200),
                    n_rounds_matchs=min(abs(match.n_rounds_matchs), 10000),
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
        username = decode_token['userID']
        if (str(decode_token["expiry"]) < str(datetime.now())):
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
