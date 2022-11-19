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
        try:
            if decode_token["expiry"] > str(datetime.now()):
                matchs = select(x for x in Match)[:]
                result = [
                    {
                        "name": p.name,
                        "max_players": p.max_players,
                        "min_players": p.min_players,
                        "n_matchs": p.n_matchs,
                        "n_rounds_matchs": p.n_rounds_matchs,
                        "user_creator": p.user_creator.username,
                    }
                    for p in matchs
                ]
                commit()
            else:
                result = "Token no válido"
        except Exception as e:
            return str(e)
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
def get_match_max_players(match_id: int):
    query = select(m.max_players for m in Match if m.id == match_id)
    for i in query:
        result = i
    return result


@db_session
def get_match_min_players(match_id: int):
    query = select(m.min_players for m in Match if m.id == match_id)
    for i in query:
        result = i
    return result


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
        if (len(match_robots) < get_match_min_players(id_match)) or (
            len(match_robots) > get_match_max_players(id_match)
        ):
            msg = {
                "Status": "La cantidad de jugadores no coincide con los parámetros de la partida"
            }
            return msg
    except Exception as e:
        error = ""
        if "Match" in str(e):
            error = "La partida no existe"
        elif "User" in str(e):
            error = "El usuario no existe"
        return error
    return list(match_robots)


def parse_robots(robot_list: list):
    """Dado un arreglo de id de robots devuelve el comportamiento
    correspondiente a ese id segun el archivo .py

    Args:
        robot_list (list): Lista de valores enteros que se corresponden con
        los id de los robots en la partida

    Returns:
        robots (list): Lista de objetos cuyas clases están definidas en
        un archivo .py.
    """
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
    """Dada una lista de objetos de robots, ejecuta n_games cantidad de juegos
    con n_rounds rondas cada una, y los devuelve en un arreglo de arreglos

    Args:
        n_games (int): Cantidad de juegos a jugar en la partida
        n_rounds (int): Cantidad de rondas que cada juego va a tener
        robots (list): Lista de objetos que contiene comportamiento de los robots
        robot_id_list (list): Lista de los id de cada robot en partida

    Returns:
        outer_response (list): Arreglo de arreglos de arrreglos de objetos JSON
    """
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
    """Dado un arreglo de arreglos de arreglos de objetos JSON que representan
    la ejecucion de una partida devuelve el ultimo arreglo de objetos JSON de cada
    partida que representan la última ronda de la misma

    Args:
        outer_response (list): Arreglo de arreglos de arreglos de objetos JSON

    Returns:
        juego (list): Diccionario de valores que contiene la ultima ronda de
        cada juego.
    """
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
    """Dado un diccionario de valores que contiene la ultima ronda de cada
    juego devuelve aquellos robots que aun estén vivos en la última ronda

    Args:
        juego (list): Diccionario de valores que contiene la ultima ronda de
        cada juego

    Returns:
        resultado: Diccionario que contiene los robots vivos al final de la
        ejecucion de cada juego
    """
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
