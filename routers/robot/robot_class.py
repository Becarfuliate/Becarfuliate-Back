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
    
    
    def polar_to_rect(self,ang,distance,origin):
        
        def correct_y(origin_x,origin_y,dest_x,dest_y,x_border):
            res = ((dest_y - origin_y) / (dest_x - origin_x)) * (x_border - origin_x) + origin_y
            return res
        def correct_x(origin_x,origin_y,dest_x,dest_y,y_border):
            res = (y_border - origin_y) * ((dest_x - origin_x) / (dest_y - origin_y)) + origin_x
            return res
        
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
        
    def block_direction(self,current_direction,current_velocity,required_direction):
        if(current_velocity<=50):
            return required_direction % 360
        else:
            right_limit = (current_direction + SPIN_FACTOR) % 360
            left_limit = (current_direction + (360-SPIN_FACTOR)) % 360
            if(abs(required_direction-right_limit) <= abs(required_direction-left_limit)):
                return right_limit
            else:
                return left_limit
    
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
        (x,y) = self.polar_to_rect(self.current_direction,self.current_velocity,self.current_position)
        if (x>1000):
            x=1000
        if(y>1000):
            y=1000
        if(x<0):
            x=0
        if(y<0):
            y=0
        self.current_position = (x,y)

