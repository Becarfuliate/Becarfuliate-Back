from pony.orm import PrimaryKey, Optional, Set
from db.database import db


class Match(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str, unique=True)
    max_players = Optional(int)
    min_players = Optional(int)
    password = Optional(str)
    n_matchs = Optional(int)
    n_rounds_matchs = Optional(int)
    # users = Set('User', reverse="matchs")
    # robot_winner -> instancia de la class robot_in_match (no disponible)
    # user_creator = Required(User, reverse="match_creates")
    # robots_players -> instancia de la class robot_in_match (no disponible)
