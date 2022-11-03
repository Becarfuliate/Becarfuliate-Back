from fastapi import APIRouter
from schemas import isim
from crud import simulation_service as sc
from routers.robot.robot_class import Robot
from routers.game.game import inflingir_danio, avanzar_ronda
from crud.robot_service import get_file_by_id
from pathlib import Path
from random import randint

simulation_end_points = APIRouter()


def game(r1, r2, r3, r4, rounds):
    list_robot = [r1, r2, r3, r4]
    if None in list_robot:
        list_robot.remove(None)
    if None in list_robot:
        list_robot.remove(None)
    for robot in list_robot:
        robot.initialize()
    for i in range(rounds):
        results_by_robots = avanzar_ronda(r1, r2, r3, r4)
    return results_by_robots


@simulation_end_points.post("/simulation/add")
async def create_simulation(simulation: isim.SimulationCreate):

    id_robot_parsed = simulation.id_robot.split(",")
    cant_robots = len(id_robot_parsed)
    outer_response = []
    robots = []

    for x in id_robot_parsed:
        file = get_file_by_id(x)
        exec(
            open("routers/robots/" + file).read(),
            globals(),
        )
        r = myRobot((randint(800, 999), randint(800, 999)), 100, randint(0, 360), 10)
        print(r)
        robots.append(r)

    # ejecutar el file, traerlo todo
    # exec()

    for i in range(simulation.n_rounds_simulations):
        if cant_robots == 2:
            outer_response.append(
                game(robots[0], robots[1]), rounds=simulation.n_rounds_simulations
            )
        if cant_robots == 3:
            outer_response.append(
                game(
                    robots[0],
                    robots[1],
                    robots[2],
                    rounds=simulation.n_rounds_simulations,
                )
            )
        if cant_robots == 4:
            outer_response.append(
                game(
                    robots[0],
                    robots[1],
                    robots[2],
                    robots[3],
                    simulation.n_rounds_simulations,
                )
            )
    return outer_response
