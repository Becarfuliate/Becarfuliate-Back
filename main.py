from fastapi import FastAPI
from dependency import *
from routers.match_controller import match_end_points
from db.database import gen_map
from models import entities

app = FastAPI()
gen_map()
app.include_router(match_end_points)
