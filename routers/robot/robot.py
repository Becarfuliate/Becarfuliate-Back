from math import sqrt, degrees, atan


def amplitude_to_depth(degre):
    """
    Toma una apertura de 1 a 10 y
    retorna la profundidad en metros que se van a escanear.
    degre = 1 --> 1000m
    ...
    degre = 10 --> 100m
    """
    result = -100 * degre + 1100
    return result


def get_distance(tuple1, tuple2):
    distance = sqrt((tuple2[0] - tuple1[0]) ** 2 + (tuple2[1] - tuple1[1]) ** 2)
    return distance


def in_direction(theta, alpha, min_plus):
    is_direction = False

    if theta in range(alpha - min_plus, alpha + min_plus):
        is_direction = True

    return is_direction


class robot:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.cannon_ammo = 0
        self.required_direction = 0
        self.required_velocity = 0

        self.direction_scanner = 0
        self.resolution_in_degrees = 10
        self.scanned_list = []
        self.scanner_range = 100

    def drive(self, degree, velocity):
        self.required_direction = degree
        self.required_velocity = velocity

    # Escáner
    # Setter
    def point_scanner(self, direction, resolution_in_degrees):
        """con este método se puede apuntar el escáner en cualquier dirección.
        Pero el resultado del escaneo estará disponible en la siguiente ronda,
        a través del siguiente método.
        """
        # Set scan direction
        if direction < 0:
            direction = -direction
        elif direction >= 360:
            direction %= 360

        self.direction_scanner = direction
        self.resolution_in_degrees = resolution_in_degrees
        self.scanner_range = amplitude_to_depth(resolution_in_degrees)

    # Getter
    def scanned(self):
        """
        devuelve el resultado del escaneo de la ronda previo. Devuelve la
        distancia al robot más cercano en la dirección apuntada.
        """
        distance = self.scanned_list
        return distance

    # Setter
    def scan(self, *robots_position):

        for r_position in robots_position:
            distance_b2_points = get_distance(self.position, r_position)
            # Ya sé que está en el rango, ahora quiero ver
            # si está en la dirección
            if distance_b2_points <= self.scanner_range:
                theta_s_r = 0
                # Salvar los angulos en los que estoy en la misma pendiente,
                # sino div zero
                # pendiente
                slope = 0.0
                # Fixme: Hacer cuatro casos distintos si y1 > y0 --> abs
                if self.position[0] != r_position[0]:
                    slope = (self.position[1] - r_position[1]) / (
                        self.position[0] - r_position[0]
                    )
                # Los puntos están en la misma coordenada x,
                # chequeo que y1 <= y2
                elif self.position[1] <= r_position[1]:
                    theta_s_r = 90
                elif self.position[1] > r_position[1]:
                    theta_s_r = 270
                # x_0 <= x1 and
                if (
                    self.position[0] <= r_position[0]
                    and self.position[1] >= r_position[1]
                ):
                    # ángulo desde mí robot al otro robot
                    theta_s_r = 360 + degrees(atan(slope))
                # x_0 <= x1
                if (
                    self.position[0] <= r_position[0]
                    and self.position[1] < r_position[1]
                ):
                    # ángulo desde mí robot al otro robot
                    theta_s_r = degrees(atan(slope))
                # x_0 > x_1
                if self.position[0] > r_position[0]:
                    # La suma acá la introduje yo, la formula original es resta.
                    theta_s_r = 180 + degrees(atan(slope))
                if in_direction(
                    theta_s_r, self.direction_scanner, self.resolution_in_degrees
                ):
                    self.scanned_list.append(r_position)


# Caso que cae en div por zero
r1 = robot((500, 490), 90)
r2 = robot((500, 500), 90)
r1.point_scanner(90, 10)
r1.scan(r2.position)
escaneado = r1.scanned()
print(escaneado)

r1 = robot((500, 490), 90)
r2 = robot((400, 490), 90)
r1.point_scanner(180, 10)
r1.scan(r2.position)
escaneado = r1.scanned()
print(escaneado)

# Este caso lo rompe
r1 = robot((500, 600), 90)
r2 = robot((600, 500), 90)
r1.point_scanner(315, 3)
r1.scan(r2.position)
escaneado = r1.scanned()
print(escaneado)

# Caso cuadrante 3
r1 = robot((500, 500), 90)
r2 = robot((600, 600), 90)
r1.point_scanner(45, 3)
r1.scan(r2.position)
escaneado = r1.scanned()
print(escaneado)

# Caso que anda
r1 = robot((600, 600), 90)
r2 = robot((500, 500), 90)
r1.point_scanner(225, 9)
r1.scan(r2.position)
escaneado = r1.scanned()
print(escaneado)
