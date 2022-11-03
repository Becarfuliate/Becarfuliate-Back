from fastapi import APIRouter
from schemas import isim
from crud import simulation_service as sc
from routers.robot.robot_class import Robot
from routers.game.game import inflingir_danio, avanzar_ronda
from crud.robot_service import get_file_by_id

simulation_end_points = APIRouter()

def game(r1, r2, r3, r4, rounds):
    list_robot = [r1, r2, r3, r4]
    print(list_robot)
    if None in list_robot:
        list_robot.remove(None)
    for i in range(rounds):
        results_by_robots = avanzar_ronda(r1, r2, r3, r4)
    return results_by_robots


@simulation_end_points.post("/simulation/add")
async def create_simulation(simulation: isim.SimulationCreate):

    id_robot_parsed = simulation.id_robot.split(",")
    cant_robots = len(id_robot_parsed)
    outer_response = []

    for x in id_robot_parsed:
        file = get_file_by_id(x)
        # ejecutar el file, traerlo todo
        #exec()

    for i in range(simulation.n_rounds_simulations):
        if cant_robots == 2:
            outer_response.append(game(id_robot_parsed[0], id_robot_parsed[1]))
            print("Mando 2")
        if cant_robots == 3:
            print("Mando 3")
            outer_response.append(
                game(
                    id_robot_parsed[0],
                    id_robot_parsed[1],
                    id_robot_parsed[2],
                )
            )
        if cant_robots == 4:
            print("Mando 4")
            outer_response.append(
                game(
                    id_robot_parsed[0],
                    id_robot_parsed[1],
                    id_robot_parsed[2],
                    id_robot_parsed[3],
                )
            )
    return outer_response
