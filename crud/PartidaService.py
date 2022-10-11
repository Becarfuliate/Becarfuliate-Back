from pony.orm import db_session
from schemas import IPartidas
from models.Partidas import Partida


@db_session
def create_partida(partida):
    Partida(
        nombre=partida.nombre,
        max_jugadores=partida.max_jugadores,
        min_jugadores=partida.min_jugadores,
        contrasenia=partida.contrasenia,
        nro_juegos=partida.nro_juegos,
        nro_rondas_juego=partida.nro_rondas_juego,
    )
