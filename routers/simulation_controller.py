from fastapi import APIRouter
from schemas import isim
from crud import simulation_service as sc
from routers.robot.game import Robot, inflingir_danio

simulation_end_points = APIRouter()


def avanzar_ronda(
    r1: Robot = None, r2: Robot = None, r3: Robot = None, r4: Robot = None
):
    robots = [r1, r2, r3, r4]
    json_response = []
    robot1 = {
        "id": None,  # Se carga afuera
        "imagen": None,  # Se carga afuera
        "x": 0,
        "y": 0,
        "xf": 0,
        "yf": 0,
        "nombre": None,  # Se carga afuera
        "vida": 100,
        "mira": (0, 0),
        "motor": 0,
        "xmis": 0,
        "ymis": 0,
        "xmisf": 0,
        "ymisf": 0,
    }
    robot2 = {
        "id": None,  # Se carga afuera
        "imagen": None,  # Se carga afuera
        "x": 0,
        "y": 0,
        "xf": 0,
        "yf": 0,
        "nombre": None,  # Se carga afuera
        "vida": 100,
        "mira": (0, 0),
        "motor": 0,
        "xmis": 0,
        "ymis": 0,
        "xmisf": 0,
        "ymisf": 0,
    }
    robot3 = {
        "id": None,  # Se carga afuera
        "imagen": None,  # Se carga afuera
        "x": 0,
        "y": 0,
        "xf": 0,
        "yf": 0,
        "nombre": None,  # Se carga afuera
        "vida": 100,
        "mira": (0, 0),
        "motor": 0,
        "xmis": 0,
        "ymis": 0,
        "xmisf": 0,
        "ymisf": 0,
    }
    robot4 = {
        "id": None,  # Se carga afuera
        "imagen": None,  # Se carga afuera
        "x": 0,
        "y": 0,
        "xf": 0,
        "yf": 0,
        "nombre": None,  # Se carga afuera
        "vida": 100,
        "mira": (0, 0),
        "motor": 0,
        "xmis": 0,
        "ymis": 0,
        "xmisf": 0,
        "ymisf": 0,
    }
    if None in robots:
        robots.remove(None)
    json_response.append(robot1)
    json_response.append(robot2)
    if len(robots) == 3:
        print("Meti 3")
        json_response.append(robot3)
    if len(robots) == 4:
        print("Meti 4")
        json_response.append(robot3)
        json_response.append(robot4)

    return json_response


def game(
    r1: Robot = None,
    r2: Robot = None,
    r3: Robot = None,
    r4: Robot = None,
    rounds: int = 2,
):
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
