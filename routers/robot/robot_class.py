from math import sin, cos, pi
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

    def _polar_to_rect(self,ang,distance,origin):

        def correct_y(origin_x,origin_y,dest_x,dest_y,x_border):
            res = ((dest_y - origin_y) / (dest_x - origin_x)) * (x_border - origin_x) + origin_y
            return int(res)
        def correct_x(origin_x,origin_y,dest_x,dest_y,y_border):
            res = (y_border - origin_y) * ((dest_x - origin_x) / (dest_y - origin_y)) + origin_x
            return int(res)

        if(distance==0):
            return (origin[0],origin[1])

        radian = float(ang * pi /180) 
        x = round(origin[0] + distance * cos(radian))
        y = round(origin[1] + distance * sin(radian))

        if (x<0 or x>1000 or y<0 or y>1000):
            if(ang == 90):
                return (x,1000)
            if(ang ==270):
                return (x,0)
            if (ang==0):
                return (1000,y)
            if (ang==180):
                return (0,y)
            #cuadrante izq
            if(x<=y and x<= -y + 1000):
                corrected_y = correct_y(origin[0],origin[1],x,y,0)
                return (0,corrected_y)
            #cuadrante superior
            elif(x<=y and not x<= -y + 1000):
                corrected_x = correct_x(origin[0],origin[1],x,y,1000)
                return (corrected_x,1000)
            #cuadrante derecho
            elif(not x<=y and not x<= y- 1000):
                corrected_y = correct_y(origin[0],origin[1],x,y,1000)
                return (1000,corrected_y)
            #cuadrante inferior
            else:
                #not x<=y and x<=-y+1000
                corrected_x = correct_x(origin[0],origin[1],x,y,0)
                return (corrected_x,0)
        else:
            return (x,y)

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
