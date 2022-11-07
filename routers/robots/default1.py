from routers.robot.robot_class import Robot
from random import randint


class default1(Robot):
    def initialize(self):
        pass
    def respond(self):
        #direction = self.get_direction()
        self.point_scanner(180,2)
        scaned = -1
        scaned = self.scanned()
        if (scaned != -1) and (scaned < 1000):
            self.cannon(180,scaned)
        #if(direction==0):
        #    self.drive(90,20)
            #self.point_scanner(90,10)
            #if(len(scaned)>0):
            #    self.cannon(270,scaned[0])
        #elif(direction==90):
        #    self.drive(180,20)
            #self.point_scanner(180,10)
            #if(len(scaned)>0):
            #    self.cannon(0,scaned[0])
        #elif(direction==180):
        #    self.drive(270,20)
            #self.point_scanner(270,10)
            #if(len(scaned)>0):
            #    self.cannon(90,scaned[0])
        #elif(direction ==  270):
        #    self.drive(0,20)
            #self.point_scanner(0,10)
            #if(len(scaned)>0):
            #    self.cannon(270,scaned[0])
        #else:
        #    self.drive(90,20)
            #self.point_scanner(90,10)
