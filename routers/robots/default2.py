from routers.robot.robot_class import Robot
from random import randint


class default2(Robot):
    def initialize(self):
        pass

    def respond(self):
        self.cannon(40, 300)
        self.drive(randint(0, 360), randint(0, 100))
