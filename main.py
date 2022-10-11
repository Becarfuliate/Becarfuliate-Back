from fastapi import FastAPI
from dependency import *

# configuramos la bd
from db.database import db

# importamos todo lo relacionado a partidas.
from models import Matchs

# inicializamos fastapi
app = FastAPI()
db.generate_mapping(create_tables=True)

from routers import MatchController
