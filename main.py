from fastapi import FastAPI
from db.database import db
from models.Users import User
from routers.usersController import user_end_points


app = FastAPI()
db.generate_mapping(create_tables=True)
app.include_router(user_end_points)