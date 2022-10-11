from fastapi import FastAPI
from dependency import *
from fastapi import APIRouter

# configuramos la bd
from db.database import db

# importamos todo lo relacionado a partidas.
from models import Partidas

# inicializamos fastapi
app = FastAPI()
router = APIRouter()
db.generate_mapping(create_tables=True)

from routers import PartidaController
