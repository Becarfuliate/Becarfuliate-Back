from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dependency import *
from routers.match_controller import match_end_points
from db.database import gen_map
from models import entities


app = FastAPI()
# Agregando cors urls
origins = ["http://localhost:3000", "localhost:3000"]
# Agregando middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
gen_map()
app.include_router(match_end_points)
