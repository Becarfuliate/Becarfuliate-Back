from math import sin, cos, pi
from typing import Tuple
from decouple import config

ACELERATION_FACTOR = int(config("aceleration"))
MAX_VELOCITY = int(config("maxvelocity"))
SPIN_FACTOR = int(config("spinFactor"))


class Robot:
    def __init__(
        self,
        position: tuple = None,
        damage: int = None,
        direction: int = None,
        velocity: int = None,
    ):
        self.current_position = position
        self.current_damage = damage
        self.current_direction = direction
        self.current_velocity = velocity
        self.cannon_ammo = 1
        self.required_direction = 0
        self.required_velocity = 0
        self.cannon_degree = 0
        self.cannon_distance = 0
        self.cannon_shoot = False
        self.misil_position = (None, None)

    # Cañón
    def is_cannon_ready(self):
        """Cuando se dispara un misil, el cañón requiere un tiempo
        para recargarse. Se puede usar esta función para chequear si
        el cañón está completamente recargado"""
        return self.cannon_ammo == 1

    def drive(self, degree, velocity):
        self.required_direction = degree
        self.required_velocity = velocity

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
        self.cannon_shoot = True
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

    def polar_to_rect(self, ang, distance, origin):
        def correct_y(origin_x, origin_y, dest_x, dest_y, x_border):
            res = ((dest_y - origin_y) / (dest_x - origin_x)) * (
                x_border - origin_x
            ) + origin_y
            return int(res)

        def correct_x(origin_x, origin_y, dest_x, dest_y, y_border):
            res = (y_border - origin_y) * (
                (dest_x - origin_x) / (dest_y - origin_y)
            ) + origin_x
            return int(res)

        if distance == 0:
            return (origin[0], origin[1])

        radian = float(ang * pi / 180)
        x = round(origin[0] + distance * cos(radian))
        y = round(origin[1] + distance * sin(radian))

        if x < 0 or x > 999 or y < 0 or y > 999:
            if ang == 90:
                return (x, 999)
            if ang == 270:
                return (x, 0)
            if ang == 0 or ang == 360:
                return (999, y)
            if ang == 180:
                return (0, y)
            # cuadrante izq
            if x < 0:
                corrected_y = correct_y(origin[0], origin[1], x, y, 0)
                corrected_x = correct_x(origin[0], origin[1], x, y, 0)
                if y < 0 and corrected_x > 0 and corrected_x < 1000:
                    # Entonces estoy en el inferior
                    return (corrected_x, 0)
                elif y > 1000 and corrected_x > 0 and corrected_x < 1000:
                    # Entonces estoy en el superior
                    return (corrected_x, 999)
                return (0, abs(corrected_y))
            # cuadrante superior
            elif y > 999:
                corrected_x = correct_x(origin[0], origin[1], x, y, 1000)
                corrected_y = correct_y(origin[0], origin[1], x, y, 1000)
                if x > 999 and corrected_y > 0 and corrected_y < 1000:
                    # Estoy en el derecho
                    return (999, corrected_y)
                elif x < 0 and corrected_y > 0 and corrected_y < 1000:
                    # Estoy en el izquierdo
                    return (0, corrected_y)
                return (abs(corrected_x), 999)
            # cuadrante derecho
            elif x > 999:
                corrected_y = correct_y(origin[0], origin[1], x, y, 1000)
                corrected_x = correct_x(origin[0], origin[1], x, y, 0)
                if y < 0 and corrected_x > 0 and corrected_x < 1000:
                    # Estoy en el inferior
                    return (corrected_x, 0)
                elif y > 999 and corrected_x > 0 and corrected_x < 1000:
                    # Estoy en el superior
                    return (corrected_x, 999)
                return (999, abs(corrected_y))
            # cuadrante inferior
            else:
                # not x<=y and x<=-y+1000
                corrected_x = correct_x(origin[0], origin[1], x, y, 0)
                corrected_y = correct_y(origin[0], origin[1], x, y, 1000)
                if x > 999 and corrected_y > 0 and corrected_y < 1000:
                    # Estoy en el derecho
                    return (999, corrected_y)
                elif x < 0 and corrected_y > 0 and corrected_y < 1000:
                    # Estoy en el izquierdo
                    corrected_y = correct_y(origin[0], origin[1], x, y, 0)
                    return (0, corrected_y)
                return (abs(corrected_x), 0)
        else:
            return (x, y)

    def shoot(self):
        misil_target = (None, None)
        if self.is_cannon_ready() and self.cannon_shoot:
            self.cannon_ammo = 0
            misil_target = self.polar_to_rect(
                ang=self.cannon_degree,
                distance=self.cannon_distance,
                origin=self.current_position,
            )
        else:
            self.cannon_ammo += 1
        self.misil_position = misil_target
        return misil_target

    def block_direction(self, current_direction, current_velocity, required_direction):
        new_direction = required_direction % 360
        if new_direction < 0:
            new_direction = new_direction + 360
        if current_velocity <= 50:
            return new_direction
        else:
            right_limit = (current_direction - SPIN_FACTOR) % 360
            left_limit = (current_direction + SPIN_FACTOR) % 360
            if new_direction < right_limit:
                return right_limit
            elif new_direction > left_limit:
                return left_limit
            else:
                return new_direction

    def calc_velocity(self, required_velocity, current_velocity):
        # sanitize input
        if required_velocity > 100:
            new_velocity = 100
        elif required_velocity < 0:
            new_velocity = 0
        else:
            new_velocity = required_velocity

        # calc velocity
        if new_velocity < current_velocity:
            decrease = (MAX_VELOCITY - new_velocity) * ACELERATION_FACTOR / MAX_VELOCITY
            if decrease < 0:
                decrease = 0
            return current_velocity - decrease
        else:
            increase = new_velocity * ACELERATION_FACTOR / MAX_VELOCITY
            if increase > MAX_VELOCITY:
                increase = MAX_VELOCITY
            return current_velocity + increase

    def move(self):
        # seting direction
        self.current_direction = self.block_direction(
            self.current_direction, self.current_velocity, self.required_direction
        )
        # seting velocity
        self.current_velocity = self.calc_velocity(
            self.required_velocity, self.current_velocity
        )
        # seting position
        self.current_position = self.polar_to_rect(
            self.current_direction, self.current_velocity, self.current_position
        )
