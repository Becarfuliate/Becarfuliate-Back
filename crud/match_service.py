from datetime import datetime
# from types import NoneType
from pony.orm import db_session, commit, select, left_join
from schemas import imatch
from models.entities import Match, User
from crud.user_services import decode_JWT, encrypt_password, search_user_by_email
import re


def is_email(user_crator: str):
    """Chequea que user_creator sea un email correcto.

    Args:
        user_crator (str): username o email.

    Returns:
        bool: True si user_crator es un email válido.
    """
    regex = (
        r"[a-zA-Z0-9_.-]+[^!#$%^&*()]@(?:gmail"
        r"|hotmail|yahoo|live|mi.unc|outlook)\.(?:com|es|edu.ar)"
    )
    result = isinstance(re.search(regex, user_crator), re.Match)
    return result


def is_username(user_creator: str):
    """Chequea que user_creator sea un username válido.

    Args:
        user_creator (str): username o email

    Returns:
        bool: True si user_creator es un username válido.
    """
    result = True
    if user_creator == "":
        resutl = False
    if " " in user_creator:
        result = False
    if len(user_creator) > 40:
        result = False
    return result


def find_by_username_or_email(user_creator: str):
    """Busca un usuario por username o email

    Args:
        user_creator (str): username o email.

    Raises:
        Exception: _description_

    Returns:
        Any: Error
        User: Retorna el usuario.
    """
    if is_email(user_creator):
        result = search_user_by_email(user_creator)
        if isinstance(result, NoneType):
            raise Exception
    elif is_username(user_creator):
        result = User[user_creator]
    return result


@db_session
def create_match(match: imatch.MatchCreate):
    """Crea una partida

    Args:
        match (imatch.MatchCreate): Valores de la partida a crear.

    Returns:
        str: retorna un string de error o validando la partida agregada.
    """
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
    """Listar Partidas

    Args:
        token (str): token

    Returns:
        str: En caso de error
        List[Match]: Lista de partidas.
    """
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
    """Lista una partida.

    Args:
        id_match (int): id de la partida a listar.

    Returns:
        str: En caso de error.
        Match: Devuelve la partida.
    """
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
    """Devuelve el id de una partida.

    Args:
        match_name (str): nombre de la partida

    Returns:
        Any: 
        None:
    """
    result = select(m.id for m in Match if m.name == match_name)
    for i in result:
        return i


@db_session
def read_match_players(id_match: int):
    """Lista los jugadores de la partida

    Args:
        id_match (int): id de la partida

    Returns:
        Query: Consulta con la lista de jugadores de partida.
    """
    result = select(m.users for m in Match if m.id == id_match)
    return result


@db_session
def add_player(id_match: int, name_user: str):
    """Agregar un jugador a la partida

    Args:
        id_match (int): id de la partida.
        name_user (str): username del jugador a agregar.

    Returns:
        str: Mensaje de retorno.
    """
    try:
        result = ""
        match = Match[id_match]
        user = User[name_user]
        count = len(match.users)
        if count >= 4:
            result = "La partida esta llena"
        else:
            match.users.add(user)
            result = "El usuario fue agregado a la partida"
    except Exception as e:
        error = ""
        if "Match" in str(e):
            error = "La partida no existe"
        elif "User" in str(e):
            error = "El usuario no existe"
        return error
    return result


@db_session
def remove_player(id_match: int, name_user: str):
    """Quita un jugador de una partida

    Args:
        id_match (int): id del jugador a quitar.
        name_user (str): username del jugador a quitar

    Returns:
        str: Mensaje de retorno.
    """
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
