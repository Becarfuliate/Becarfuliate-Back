from robot.robot_class import Robot

def distance(t1: tuple, t2: tuple):
    return round(((t1[0] - t2[0])**2 + (t1[1] - t2[1])**2)**0.5)


def danio_misil(robot_position: tuple, misil_position: tuple):
    if (distance(robot_position, misil_position) <= 5):
        danio = 10
    elif (distance(robot_position, misil_position) <= 20):
        danio = 5
    elif (distance(robot_position, misil_position) <= 40):
        danio = 3
    else:
        danio = 0
    return danio


def danio_colision(pos_r1: tuple, pos_r2: tuple):
    danio = (0, 0)
    if distance(pos_r1, pos_r2) <= 20:
        danio = (2,2)
    return danio

def danio_pared(pos_r: tuple):
    danio = 0
    if (pos_r[0] == 0) or (pos_r[0] == 1000):
        danio = 2
    if (pos_r[1] == 0) or (pos_r[1] == 1000):
        danio = 2
    return danio

def inflingir_danio(
    r1: Robot = None,
    r2: Robot = None,
    r3: Robot = None,
    r4: Robot = None
):
    list_robot = [r1, r2, r3, r4]
    list_robot_aux = [r1, r2, r3, r4]
    for robot in list_robot:
        list_robot = list_robot[1:]
        danio_p = danio_pared(robot.current_position)
        robot.current_damage -= danio_p
        for robot_check in list_robot:
            danio_c = danio_colision(robot.current_position, robot_check.current_position)
            robot.current_damage -= danio_c[0]
            robot_check.current_damage -= danio_c[1]
        for robot_x in list_robot_aux:
            # Revisar daño por misil
            if robot.current_velocity < 80:
                danio2 = danio_misil(robot.current_position, robot_x.misil_position)
                robot.current_damage -= danio2
                if danio2 > 0:
                    print("Pego un misil")


def check_robots_alive(l_robots: list(Robot)):
    list_clean = []
    for robot in l_robots:
        if robot.current_damage > 0:
            list_clean.append(robot)
    return list_clean 


def avanzar_ronda(
    r1: Robot = None,
    r2: Robot = None,
    r3: Robot = None,
    r4: Robot = None,
):
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
            "id": None, # Se carga afuera
            "imagen": None, # Se carga afuera
            "x": inic_pos_x, 
            "y": inic_pos_y,
            "xf": robot.current_position[0], 
            "yf": robot.current_position[1],
            "nombre": None, # Se carga afuera
            "vida": robot.current_damage, 
            "mira": robot.current_direction, 
            "motor": robot.current_velocity,
            "xmis": inic_pos_x,
            "ymis": inic_pos_y,
            "xmisf": robot.misil_position[0],
            "ymisf": robot.misil_position[1]
        }
        results_by_robots.append(result_round)
    return results_by_robots
