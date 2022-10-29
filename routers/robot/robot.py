class robot:
    def __init__(self,position,direction):
        self.required_direction= 0
        self.required_velocity = 0
    
    def drive(self,degree,velocity):
        self.required_direction = degree
        self.required_velocity = velocity