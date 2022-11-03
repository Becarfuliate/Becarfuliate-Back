"""
from routers.robot.game import Robot, inflingir_danio


def check_robots_alive(l_robots: list(Robot)):
    list_clean = []
    for robot in l_robots:
        if robot.current_damage > 0:
            list_clean.append(robot)
    return list_clean


def game(
    r1: Robot = None,
    r2: Robot = None,
    r3: Robot = None,
    r4: Robot = None,
    rounds: int = 2,
):
    json_response = []
    list_robot = [r1, r2, r3, r4]
    # Remover en el caso de no haber pasado 4 robots
    list_robot.remove(None)
    list_robot.remove(None)
    list_robot_alive = list_robot
    for robot in list_robot:
        robot.initialize()
    for round in rounds:
        results_by_robots = []
        list_robot_alive = check_robots_alive(list_robot_alive)
        inflingir_danio(r1, r2, r3, r4)
        for robot in list_robot_alive:
            robot.respond
        for robot in list_robot_alive:
            # Escanear->Atacar->Mover (Con metodos privados)
            inic_pos_x = robot.current_position[0]
            inic_pos_y = robot.current_position[1]
            robot._scan
            robot._shoot
            robot._drive
            # Inicializamos las variables
            result_round = {
                "id": None,  # Se carga afuera
                "imagen": None,  # Se carga afuera
                "x": inic_pos_x,
                "y": inic_pos_y,
                "xf": robot.current_position[0],
                "yf": robot.current_position[1],
                "nombre": None,  # Se carga afuera
                "vida": robot.current_damage,
                "mira": robot.current_direction,
                "motor": robot.current_velocity,
                "xmis": inic_pos_x,
                "ymis": inic_pos_y,
                "xmisf": robot.misil_position[0],
                "ymisf": robot.misil_position[1],
            }
            results_by_robots.append(result_round)
        json_response.append({"robots": results_by_robots})
    return json_response
"""
