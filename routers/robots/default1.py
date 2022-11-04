from routers.robot.robot_class import Robot
from random import randint


class default1(Robot):
    def initialize(self):
        pass

    def respond(self):
        self.cannon(20, 300)
        self.drive(randint(0, 360), randint(0, 100))
