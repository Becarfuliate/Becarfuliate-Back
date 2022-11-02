class RobotMadre:

        def init(self,position: tuple = None,damage: int = None,direction: int = None,velocity: int = None):
            self.current_position = position
            self.current_damage = 0
            self.current_direction = direction
            self.current_velocity = velocity
            self.required_position = (0,0)
            self.required_direction = 0
            self.required_velocity = 0
            self.direction_scaner = 0
            self.resolution_in_degrees = 10
            self.scanned_list = []
            self.scanner_range = 100
            self.cannon_degree = 0
            self.cannon_distance = 0
            self.cannon_ammo = 1
            self.cannon_shoot = False             
            self.misil_position = (0,0)


        def _scan(self):
            self.scanned_list = []
        def _shoot(self):
            self.cannon_ammo = 
            self.misil_position = (0,0)
        def _drive(self):
            self.current_position = self.required_position
            self.current_velocity = self.required_velocity
            self.current_direction = self.required_direction

class Robot(RobotMadre):
        def respond():
            a=a

def inflingir_danio(r1, r2, r3, r4):
    a=a


def check_robots_alive(l_robots: list(Robot)):
    list_clean = []
    for robot in l_robots:
        if robot.current_damage > 0:
            list_clean.append(robot)
    return list_clean 


def avanzar_ronda(
    r1: Robot = None,
    r2: Robot = None,
    r3: Robot = None,
    r4: Robot = None,
):
    results_by_robots = []
    list_robot_alive = check_robots_alive(list_robot_alive)
    inflingir_danio(r1, r2, r3, r4)
    for robot in list_robot_alive:
        robot.respond
    for robot in list_robot_alive:   
        # Escanear->Atacar->Mover (Con metodos privados)
        inic_pos_x = robot.current_position[0]
        inic_pos_y = robot.current_position[1]
        robot._scan
        robot._shoot
        robot._drive
        # Inicializamos las variables
        result_round = {
            "id": None, # Se carga afuera
            "imagen": None, # Se carga afuera
            "x": inic_pos_x, 
            "y": inic_pos_y,
            "xf": robot.current_position[0], 
            "yf": robot.current_position[1],
            "nombre": None, # Se carga afuera
            "vida": robot.current_damage, 
            "mira": robot.current_direction, 
            "motor": robot.current_velocity,
            "xmis": inic_pos_x,
            "ymis": inic_pos_y,
            "xmisf": robot.misil_position[0],
            "ymisf": robot.misil_position[1]
        }
        results_by_robots.append(result_round)
    return results_by_robots
