from fastapi import FastAPI
from db.database import db, gen_map
from models.Entities import User, Robot, Match
from routers.UsersController import user_end_points
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Agregando cors urls
origins = [
    'http://localhost:3000',
    'localhost:3000'
    ]
# Agregando middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gen_map()
app.include_router(user_end_points)
