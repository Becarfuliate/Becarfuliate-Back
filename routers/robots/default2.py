from routers.robot.robot_class import Robot
from random import randint


class default2(Robot):
    def initialize(self):
        self.round = 0
        pass

    def respond(self):
        #self.cannon(40, 300)
        self.round += 1
        if (self.round >= 4):
            self.drive(0,100) 
        pass
