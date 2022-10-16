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
