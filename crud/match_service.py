from pony.orm import db_session, commit
from schemas import imatch
from models.entities import Match


@db_session
def create_match(match: imatch.MatchCreate):
    with db_session:
        try:
            Match(
                name=match.name,
                max_players=match.max_players,
                min_players=match.min_players,
                password=match.password,
                n_matchs=min(match.n_matchs, 200),
                n_rounds_matchs=min(match.n_rounds_matchs, 10000),
            )
            commit()
        except Exception as e:
            return str(e)
        return "added"
