from pydantic import BaseModel


class Match_base(BaseModel):
    name: str
    max_players: int
    min_players: int
    password: str
    n_matchs: int
    n_rounds_matchs: int


class Match_create(Match_base):
    class Config:
        orm_mode = True


class Match(Match_base):
    id: int

    class Config:
        orm_mode = True
