from routers.robot.robot_class import Robot

class myRobot(Robot):
    def initialize(self):
        self.drive(40,40)
    def respond(self):
        self.cannon(20,300)
        self.drive(100,80)