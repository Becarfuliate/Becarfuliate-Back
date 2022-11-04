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
    for robot in list_robot:
        if robot != None:
            robot.initialize()
    for i in range(rounds):
        results_by_robots = avanzar_ronda(
            list_robot[0], list_robot[1], list_robot[2], list_robot[3]
        )
    return results_by_robots


@simulation_end_points.post("/simulation/add")
async def create_simulation(simulation: isim.SimulationCreate):
    id_robot_parsed = simulation.id_robot.split(",")
    cant_robots = len(id_robot_parsed)
    outer_response = []
    robots = []
    for x in id_robot_parsed:
        file = get_file_by_id(x)
        filename = (
            "routers/robots/"
            + file.strip(".py")
            + "_"
            + simulation.user_creator
            + ".py"
        )
        print(filename)
        exec(
            open(filename).read(),
            globals(),
        )
        file = file.strip(".py")
        klass = globals()[file]
        r = klass((randint(1, 999), randint(1, 999)), 100, randint(0, 360), 10)
        robots.append(r)
    for i in range(simulation.n_rounds_simulations):

        if cant_robots == 2:
            outer_response.append(
                game(
                    robots[0],
                    robots[1],
                    None,
                    None,
                    rounds=simulation.n_rounds_simulations,
                )
            )

        if cant_robots == 3:
            outer_response.append(
                game(
                    robots[0],
                    robots[1],
                    robots[2],
                    None,
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
            for i in outer_response:
                k = 0
                for j in i:
                    j["id"] = id_robot_parsed[k]
                    j["nombre"] = sc.get_robot_name(id_robot_parsed[k])
                    k += 1
    return outer_response
