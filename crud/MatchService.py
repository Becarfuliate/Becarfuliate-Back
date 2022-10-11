from pony.orm import db_session
from schemas import IMatchs
from models.Matchs import Match


@db_session
def create_match(match):
    Match(
        name=match.name,
        max_players=match.max_players,
        min_players=match.min_players,
        password=match.password,
        n_matchs=match.n_matchs,
        n_rounds_matchs=match.n_rounds_matchs,
    )


@db_session
def read_matchs():
    with db_session:
        matchs = Match.select()
        result = [IMatchs.Match.from_orm(p) for p in matchs]
    return result


@db_session
def read_match(id_match: int):
    with db_session:
        match = Match[id_match]
        result = IMatchs.Match.from_orm(match)
    return result
