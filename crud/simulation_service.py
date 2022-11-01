from fastapi import APIRouter, HTTPException
from pony.orm import db_session, commit, select
from schemas import isim
from models.entities import Match, User, Robot

@db_session
def check_robot(id):
    return Robot.exists(id=id)

@db_session
def check_user(username):
    return User.exists(username=username)

@db_session
def get_robot_name(id_robot):
    robots = select(r.name for r in Robot if r.id == id_robot)
    for i in robots:
        return i

@db_session
def get_robot_avatar(id_robot):
    robots = select(r.avatar for r in Robot if r.id == id_robot)
    for i in robots:
        return i