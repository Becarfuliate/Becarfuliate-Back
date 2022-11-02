from decouple import config
from math import sin,cos,pi

ACELERATION_FACTOR = int(config("aceleration"))
MAX_VELOCITY = int(config("maxvelocity"))
SPIN_FACTOR = int(config("spinFactor"))
class robot :
    
    def __init__(self,position,direction):
        
        self.current_position = position
        self.current_velocity = 0
        self.current_direction = direction
        self.required_velocity = 0
        self.required_direction = 0
    
    
    def polar_to_rect(self, ang, distance, origin):
 
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
        
    def block_direction(self,current_direction,current_velocity,required_direction):
        new_direction = required_direction % 360
        if (new_direction<0):
            new_direction = new_direction + 360
        if(current_velocity<=50):
            return new_direction
        else:
            right_limit = (current_direction - SPIN_FACTOR) % 360
            left_limit = (current_direction + SPIN_FACTOR) % 360
            if(new_direction < right_limit):
                return right_limit
            elif(new_direction> left_limit):
                return left_limit
            else:
                return new_direction
    
    def calc_velocity(self,required_velocity,current_velocity):
        #sanitize input
        if(required_velocity >100):
            new_velocity = 100
        elif(required_velocity <0):
            new_velocity = 0
        else:
            new_velocity = required_velocity
        
        #calc velocity
        if(new_velocity < current_velocity):
            decrease = ((MAX_VELOCITY-new_velocity) * ACELERATION_FACTOR/MAX_VELOCITY)
            if (decrease < 0):
                decrease = 0
            return current_velocity - decrease 
        else:
            increase = new_velocity * ACELERATION_FACTOR/MAX_VELOCITY
            if (increase > MAX_VELOCITY):
                increase = MAX_VELOCITY                
            return current_velocity + increase  

    def _move(self):
        #seting direction 
        self.current_direction = self.block_direction(self.current_direction,self.current_velocity,self.required_direction)
        #seting velocity
        self.current_velocity = self.calc_velocity(self.required_velocity,self.current_velocity)
        #seting position
        self.current_position = self.polar_to_rect(self.current_direction,self.current_velocity,self.current_position)

