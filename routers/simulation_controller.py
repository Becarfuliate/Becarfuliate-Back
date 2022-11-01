from fastapi import APIRouter
from schemas import isim
from crud import simulation_service as sc

simulation_end_points = APIRouter()


@simulation_end_points.post("/simulation/add")
async def create_simulation(simulation: isim.SimulationCreate):

    id_robot_parsed = simulation.id_robot.split(",")
    cant_robots = len(id_robot_parsed)
    outer_response = {}
    inner_response = []

    for i in range(simulation.n_rounds_simulations):
        index_ronda = "Ronda " + str(i)
        for i in range(cant_robots):
            temp = {
                "id": id_robot_parsed[i],
                "name": sc.get_robot_name(int(id_robot_parsed[i])),
                "avatar": sc.get_robot_avatar(int(id_robot_parsed[i])),
            }
            inner_response.append(temp)
        outer_response[index_ronda] = inner_response
        inner_response = []
    return outer_response
