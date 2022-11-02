from math import radians, sqrt, cos, sin, atan2, degrees


def amplitude_to_depth(degre):
    """
    Toma una apertura de 1 a 10 y
    retorna la profundidad en metros que se van a escanear.
    """
    result = -100 * degre + 1100
    return result


def cart_to_polar(x, y):
    """
    Cartesian (x, y) → Polar (r, θ)
    Convierte coordenadas cartesianas en coordenadas polares
    Siendo r el radio y theta el grado.
    Retorna grados no radianes:
        (r = 9.4352, theta = 45°)
    """
    r = sqrt(x**2 + y**2)
    theta = atan2(y, x)
    return (r, degrees(theta))


def polar_to_cart(r, theta):
    """
    Polar (r, θ) → Cartesian (x, y)
    Convierte coordenadas polares en coordenadas cartesianas.
    Retorna grados, no radianes.
    """
    theta = radians(theta)
    x = r * cos(theta)
    y = r * sin(theta)
    return (x, y)


def get_distance(tuple1, tuple2):
    distance = sqrt((tuple2[0] - tuple1[0]) ** 2 + (tuple2[1] - tuple1[1]) ** 2)
    return distance


def in_range(base_polar_cord, robot_polar_cord, point_a, point_b):
    """
    Chequea que la coordenada polar dada, esté en el rango del escáner.
    """
    is_inside = False
    # Si los grados están entre el punto a y b
    if robot_polar_cord[1] in range(point_b[1], point_a[1]):
        # Si la distancia del robot es menor a la del rango del radar
        if robot_polar_cord[0] <= base_polar_cord[0]:
            is_inside = True

    return is_inside


def check_walls(A, B):
    """
    Chequea que en la dirección y profundidad del scaner haya una pared,
    y retorna su coordenada.
    """
    coordinates = []
    if A[0] <= 0:
        coordinates.append((0, A[1]))
    elif A[0] >= 999:
        coordinates.append((999, A[1]))
    # Fix this, two cases add.
    if B[0] <= 0:
        coordinates.append((0, B[1]))
    elif B[0] >= 999:
        coordinates.append((999, B[1]))
    if A[1] <= 0:
        coordinates.append((A[0], 0))
    elif A[1] >= 999:
        coordinates.append((A[0], 999))
    # Fix this, two cases add.
    if B[1] <= 0:
        coordinates.append((B[0], 0))
    elif B[1] >= 999:
        coordinates.append((B[0], 999))

    return coordinates


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
        s_polar_cord = cart_to_polar(self.position[0], self.position[1])

        for r_position in robots_position:

            # Para cada robot tomo su cordenada polar
            # Convert coordinates in polar coordinates
            r_polar_cord = cart_to_polar(r_position[0], r_position[1])

            # a = profundidad del escaner + la dirección del robot + apertura
            # a = (500, 45° + 10°)
            point_a = (
                self.scanner_range,
                self.direction_scanner + self.resolution_in_degrees,
            )
            point_b = (
                self.scanner_range,
                self.direction_scanner - self.resolution_in_degrees,
            )
            # Ojo coor_walls puede ser una lista
            coor_walls = check_walls(polar_to_cart(point_a), polar_to_cart(point_b))
            self.scanned_list.append(coor_walls)
            # Tengo que chequear que la coordenada polar esté
            # en la misma dirección y a una distancia <= rango del escáner.
            if in_range(s_polar_cord, r_polar_cord, point_a, point_b):
                result = polar_to_cart(r_polar_cord[0], r_polar_cord[1])
                self.scanned_list.append(result)
