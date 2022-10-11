from pony.orm import PrimaryKey, Optional, Set
from db.database import db


class Partida(db.Entity):
    id = PrimaryKey(int, auto=True)
    nombre = Optional(str)
    max_jugadores = Optional(int)
    min_jugadores = Optional(int)
    contrasenia = Optional(str)
    nro_juegos = Optional(int)
    nro_rondas_juego = Optional(int)
    # usuarios = Set(Usuario, reverse="partidas")
    # robot_ganador = Set("Robot_Partida", reverse="partida_ganador")
    # usuario_creador = Required(Usuario, reverse="partidas_creadas")
    # robot_jugador = Set("Robot_Partida", reverse="partida_jugador")
