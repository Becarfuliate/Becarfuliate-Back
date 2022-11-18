from routers.robot.robot_class import Robot

class default1(Robot):
    def initialize(self):
        pass
    def respond(self):
        direction = self.get_direction()
        scaned= self.scanned()
        print(scaned)
        if(direction==0):
            self.drive(90,50)
            self.point_scanner(90,90)
            if(scaned<=3000):
                self.cannon(270,scaned)
        elif(direction==90):
            self.drive(180,50)
            self.point_scanner(180,90)
            if(scaned<=3000):
                self.cannon(0,scaned)
        elif(direction==180):
            self.drive(270,50)
            self.point_scanner(270,90)
            if(scaned<=3000):
                self.cannon(90,scaned)
        elif(direction==270):
            self.drive(0,50)
            self.point_scanner(0,90)
            if(scaned<=3000):
                self.cannon(270,scaned)
        else:
            self.drive(0,50)
            self.point_scanner(90,90)
