from pony.orm import db_session, commit
from schemas import imatch
from models.entities import Match


@db_session
def create_match(match: imatch.MatchCreate):
    with db_session:
        try:
            Match(
                name=match.name,
                max_players=abs(match.max_players),
                min_players=abs(match.min_players),
                password=match.password,
                n_matchs=min(abs(match.n_matchs), 200),
                n_rounds_matchs=min(abs(match.n_rounds_matchs), 10000),
            )
            commit()
        except Exception as e:
            return str(e)
        return "added"


def read_matchs():
    with db_session:
        try:
            matchs = Match.select()
            result = [imatch.Match.from_orm(p) for p in matchs]
            commit()
        except Exception as e:
            return str(e)
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
