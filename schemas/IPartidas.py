from pydantic import BaseModel


class PartidaBase(BaseModel):
    nombre: str
    max_jugadores: int
    min_jugadores: int
    contrasenia: str
    nro_juegos: int
    nro_rondas_juego: int


class PartidaCreate(PartidaBase):
    class Config:
        orm_mode = True


class Partida(PartidaBase):
    id: int

    class Config:
        orm_mode = True
