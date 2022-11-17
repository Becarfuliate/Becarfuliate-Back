from pony.orm import db_session, commit, select

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


@db_session
def get_robot_avatar(id_robot):
    robots = select(r.avatar for r in Robot if r.id == id_robot)
    for i in robots:
        return i


@db_session
def get_robot_id(robot_name):
    robots = select(r.id for r in Robot if r.name == robot_name)
    for i in robots:
        return i
