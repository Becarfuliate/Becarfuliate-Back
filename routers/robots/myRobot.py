from routers.robot.robot_class import Robot
from random import randint


class myRobot(Robot):
    def initialize(self):
        direction = self.get_position()

    def respond(self):
        self.cannon(20, 300)
        self.drive(100 + direction[0], 80 + direction[1])
