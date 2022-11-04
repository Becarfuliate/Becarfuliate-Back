from routers.robot.robot_class import Robot


def distance(t1: tuple, t2: tuple):
    return round(((t1[0] - t2[0]) ** 2 + (t1[1] - t2[1]) ** 2) ** 0.5)

#asdasd
def danio_misil(robot_position: tuple, misil_position: tuple):
    if misil_position == (None, None):
        return 0
    if distance(robot_position, misil_position) <= 5:
        danio = 10
    elif distance(robot_position, misil_position) <= 20:
        danio = 5
    elif distance(robot_position, misil_position) <= 40:
        danio = 3
    else:
        danio = 0
    return danio


def danio_colision(pos_r1: tuple, pos_r2: tuple):
    danio = (0, 0)
    if distance(pos_r1, pos_r2) <= 20:
        danio = (2, 2)
    return danio


def danio_pared(pos_r: tuple):
    danio = 0
    if (pos_r[0] == 0) or (pos_r[0] == 1000):
        danio = 2
    if (pos_r[1] == 0) or (pos_r[1] == 1000):
        danio = 2
    return danio


def inflingir_danio(robots:list[Robot]):
    for robot in robots:
        list_robot = robots[1:]
        danio_p = danio_pared(robot.current_position)
        robot.current_damage -= danio_p
        for robot_check in list_robot:
            danio_c = danio_colision(
                robot.current_position, robot_check.current_position
            )
            robot.current_damage -= danio_c[0]
            robot_check.current_damage -= danio_c[1]
        for robot_x in robots:
            # Revisar daño por misil
            if robot.current_velocity < 80:
                danio2 = danio_misil(robot.current_position, robot_x.misil_position)
                robot.current_damage -= danio2


def avanzar_ronda(robots:list[Robot]):
    results_by_robots = []
    inflingir_danio(robots)
    for robot in robots:
        if (robot.current_damage<=0):
            pass
        else:
            robot.respond()
    for robot in robots:
        # Escanear->Atacar->Mover (Con metodos privados)
        inic_pos_x = robot.current_position[0]
        inic_pos_y = robot.current_position[1]

        if (robot.current_damage<=0):
            result_round = {
                "id": None,  # Se carga afuera
                "imagen": None,  # Se carga afuera
                "x": inic_pos_x,
                "y": inic_pos_y,
                "xf": inic_pos_x,
                "yf": inic_pos_y,
                "nombre": None,  # Se carga afuera
                "vida": robot.current_damage,
                "mira": robot.current_direction,
                "motor": 0,
                "xmis": inic_pos_x,
                "ymis": inic_pos_y,
                "xmisf": None,
                "ymisf": None,
            }
            results_by_robots.append(result_round)
        else:
            tupla = robot.shoot()
            robot.move()

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
                "xmisf": tupla[0],
                "ymisf": tupla[1],
            }
            results_by_robots.append(result_round)
    return results_by_robots
