from distutils.sysconfig import get_makefile_filename
from pony.orm import PrimaryKey, Required, Optional
from db.database import db


class User(db.Entity):
    __table__ = "users"
    username = PrimaryKey(str, 40)
    password = Required(str, 40)
    avatar = Optional(str, nullable=False)
    confirmation_mail = Optional(bool)
    email = Required(str)