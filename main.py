from fastapi import FastAPI
from db.database import db, gen_map
from models.Entities import User, Robot, Match
from routers.UsersController import user_end_points


app = FastAPI()
gen_map()
app.include_router(user_end_points)
