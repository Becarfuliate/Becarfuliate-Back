from math import sin, cos, pi
from traceback import print_tb
from typing import Tuple


class Robot:

    def __init__(
        self,
        position: tuple = None,
        damage: int = None,
        direction: int = None,
        velocity: int = None
    ):
        self.current_position = position
        self.current_damage = damage
        self.current_direction = direction
        self.current_velocity = velocity
        self.cannon_ammo = 1
        self.required_direction = direction
        self.required_velocity = velocity
        self.required_position = position
        self.cannon_degree = 0
        self.cannon_distance = 0
        self.misil_position = position

    # Cañón
    def is_cannon_ready(self):
        """Cuando se dispara un misil, el cañón requiere un tiempo
        para recargarse. Se puede usar esta función para chequear si
        el cañón está completamente recargado"""
        return self.cannon_ammo == 1

    def cannon(self, degree, distance):
        """Cuando se llama a este método, se prepara el cañón para disparar.
        Si se llama a este método dos veces seguidas, sólo la última tiene
        efecto. Recién se ejecuta el disparo al finalizar la ronda."""
        if distance > 700:
            distance = 700
        if distance < 0:
            distance = 0
        if degree > 360:
            degree = 360
        if degree < 0:
            degree = 0
        self.cannon_degree = degree
        self.cannon_distance = distance

    # status
    def get_position(self):
        return self.current_position

    def get_velocity(self):
        return self.current_velocity

    def get_damage(self):
        return self.current_damage

    def get_direction(self):
        return self.current_direction

    def _polar_to_rect(self, ang: int, distance: int, origin: Tuple):
        radian = (ang * pi)/180
        x = round(origin[0] + distance * cos(radian))
        y = round(origin[1] + distance * sin(radian))
        print((x, y))
        return (x, y)

    def _shoot(self):
        misil_target = None
        if self.is_cannon_ready():
            self.cannon_ammo = 0
            misil_target = self._polar_to_rect(
                ang=self.cannon_degree,
                distance=self.cannon_distance,
                origin=self.current_position
            )
        else:
            self.cannon_ammo += 1
        self.misil_position = misil_target
        return misil_target


def print_status(obj1: Robot):
    print("current position", obj1.current_position)
    print("current_damage", obj1.current_damage)
    print("current_direction", obj1.current_direction)
    print("current_velocity", obj1.current_velocity)
    # print("cannon_ammo", obj1.cannon_ammo)
    # print("required_direction", obj1.required_direction)
    # print("required_velocity", obj1.required_velocity)
    # print("required_position", obj1.required_position)
    # print("cannon_degree", obj1.cannon_degree)
    # print("cannon_distance", obj1.cannon_distance)


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


# robot1 = Robot(
#     position=(1, 1),
#     damage=100,
#     direction=45,
#     velocity=40)
# robot1.misil_position=(100,100)

# robot2 = Robot(
#     position=(1, 999),
#     damage=100,
#     direction=45,
#     velocity=40)
# robot2.misil_position=(20,36)

# robot3 = Robot(
#     position=(999, 1),
#     damage=100,
#     direction=45,
#     velocity=40)
# robot3.misil_position=(10,2)

# robot4 = Robot(
#     position=(999, 999),
#     damage=100,
#     direction=45,
#     velocity=40)
# robot4.misil_position=(1,1)

# print("ROBOT 1")
# print_status(robot1)
# print("ROBOT 2")
# print_status(robot2)
# print("ROBOT 3")
# print_status(robot3)
# print("ROBOT 4")
# print_status(robot4)
# inflingir_danio(robot1, robot2, robot3, robot4)
# print("ROBOT 1")
# print_status(robot1)
# print("ROBOT 2")
# print_status(robot2)
# print("ROBOT 3")
# print_status(robot3)
# print("ROBOT 4")
# print_status(robot4)
