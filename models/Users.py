from distutils.sysconfig import get_makefile_filename
from pony.orm import PrimaryKey, Required, Optional
from db.database import db


class User(db.Entity):
    __table__ = "users"
    id = PrimaryKey(int, auto=True)
    username = Required(str, 40, unique=True)
    password = Required(str, 40)
    avatar = Optional(str, nullable=False)
    confirmation_mail = Optional(bool)
    email = Required(str, unique=True)
    # robots = Set('Robot')
    # estadisticas_robots = Set('Estadisticas_Robot')
    # partidas = Set('Partida', reverse='usuarios')
    # partidas_creadas = Set('Partida', reverse='usuario_creador')
    # simulacion = Optional('Simulacion')