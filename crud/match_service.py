from datetime import datetime
from pony.orm import db_session, commit
from schemas import imatch
from models.entities import Match, User
from crud.user_services import decode_JWT, encrypt_password


@db_session
def create_match(match: imatch.MatchCreate):
    with db_session:
        decode_token = decode_JWT(match.token)
        if decode_token["expiry"] > str(datetime.now()):
            try:
                creator_aux = User[match.user_creator].username
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
                        User[match.user_creator],
                    },
                    user_creator=User[match.user_creator],
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
