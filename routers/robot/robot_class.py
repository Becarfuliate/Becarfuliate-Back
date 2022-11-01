from math import sin, cos, pi
from typing import Tuple


class Robot:

    def __init__(
        self,
        position: tuple,
        damage: int,
        direction: int,
        velocity: int
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
            if misil_target[0] > 1000:
                misil_target = (1000,misil_target[1])
            elif misil_target[0] < 0:
                misil_target = (0,misil_target[1])
            if misil_target[1] > 1000:
                misil_target = (misil_target[0], 1000)
            elif misil_target[1] < 0:
                misil_target = (misil_target[0], 0)
        else:
            self.cannon_ammo += 1
        return misil_target


def print_status(obj1: Robot):
    print("current position", obj1.current_position)
    print("current_damage", obj1.current_damage)
    print("current_direction", obj1.current_direction)
    print("current_velocity", obj1.current_velocity)
    print("cannon_ammo", obj1.cannon_ammo)
    print("required_direction", obj1.required_direction)
    print("required_velocity", obj1.required_velocity)
    print("required_position", obj1.required_position)
    print("cannon_degree", obj1.cannon_degree)
    print("cannon_distance", obj1.cannon_distance)


obj1 = Robot(
    position=(5, 5),
    damage=100,
    direction=45,
    velocity=100)
print_status(obj1)
obj1.cannon(degree=225, distance=1000)
print("El misil va rumbo hacia:", obj1._shoot())
print_status(obj1)
