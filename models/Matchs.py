from enum import unique
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
    # users = Set(Usuario, reverse="matchs")
    # robot_winner = Set("Robot_Match", reverse="match_winner")
    # user_creator = Required(Usuario, reverse="match_creates")
    # robot_player = Set("Robot_Match", reverse="match_player")
