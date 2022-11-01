from fastapi import APIRouter, HTTPException
from pony.orm import db_session, commit, select
from schemas import isim
from models.entities import Match, User, Robot
from crud import simulation_service as sc

simulation_end_points = APIRouter()

@simulation_end_points.post("/simulation/add")
async def create_simulation(simulation: isim.SimulationCreate):

    id_robot_parsed = simulation.id_robot.split(",")
    response = []
    for i in range(len(id_robot_parsed)):
        temp = {"id": id_robot_parsed[i],
                "name": sc.get_robot_name(id_robot_parsed[i]),
                "avatar": sc.get_robot_avatar(id_robot_parsed[i])}
        response.append(temp)
        
    return {"Robot": response}

