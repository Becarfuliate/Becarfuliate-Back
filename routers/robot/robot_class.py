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
        self.cannon_shoot = False
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

    def _polar_to_rect(self, ang, distance, origin):
 
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
 
        if (x<0 or x>999 or y<0 or y>999):
            if(ang == 90):
                return (x,999)
            if(ang ==270):
                return (x,0)
            if (ang==0 or ang==360):
                return (999,y)
            if (ang==180):
                return (0,y)
            #cuadrante izq
            if(x<0):
                corrected_y = correct_y(origin[0],origin[1],x,y,0)
                corrected_x = correct_x(origin[0],origin[1],x,y,0)
                if(y<0 and corrected_x>0 and corrected_x<1000):
                    # Entonces estoy en el inferior
                    return (corrected_x,0)
                elif(y>1000 and corrected_x>0 and corrected_x<1000):
                    # Entonces estoy en el superior
                    return (corrected_x,999)
                return (0,abs(corrected_y))
            #cuadrante superior
            elif(y>999):
                corrected_x = correct_x(origin[0],origin[1],x,y,1000)
                corrected_y = correct_y(origin[0],origin[1],x,y,1000)
                if (x > 999 and corrected_y>0 and corrected_y<1000):
                    # Estoy en el derecho
                    return (999,corrected_y)
                elif (x < 0 and corrected_y>0 and corrected_y<1000):
                    # Estoy en el izquierdo
                    return (0,corrected_y)
                return (abs(corrected_x),999)
            #cuadrante derecho
            elif(x>999):
                corrected_y = correct_y(origin[0],origin[1],x,y,1000)
                corrected_x = correct_x(origin[0],origin[1],x,y,0)
                if (y<0 and corrected_x>0 and corrected_x<1000):
                    # Estoy en el inferior
                    return (corrected_x,0)
                elif (y>999 and corrected_x>0 and corrected_x<1000):
                    # Estoy en el superior
                    return (corrected_x,999)
                return (999,abs(corrected_y))
            #cuadrante inferior
            else:
                #not x<=y and x<=-y+1000
                corrected_x = correct_x(origin[0],origin[1],x,y,0)
                corrected_y = correct_y(origin[0],origin[1],x,y,1000)
                if (x>999 and corrected_y>0 and corrected_y<1000):
                    # Estoy en el derecho
                    return (999,corrected_y)
                elif (x<0 and corrected_y>0 and corrected_y<1000):
                    # Estoy en el izquierdo
                    corrected_y = correct_y(origin[0],origin[1],x,y,0)
                    return (0,corrected_y)
                return (abs(corrected_x),0)
        else:
            return (x,y)

    def _shoot(self):
        misil_target = None
        if self.is_cannon_ready() and self.cannon_shoot:
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