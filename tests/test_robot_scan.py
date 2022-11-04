from routers.robot.robot import robot


def test_1():
    """
    Test 1: Los robots están en el mismo eje x,
            pero r2, está a 10m más arriba de r1.
    """
    r1 = robot((500, 490), 90)
    r2 = robot((500, 500), 90)
    r1.point_scanner(90, 10)
    r1.scan(r2.position)
    assert r1.scanned() == [r2.position]


def test_2():
    """
    Test 2: Los robots están en el mismo eje y,
            pero r2 está a 100m a la izquierda de r1.
    """
    r1 = robot((500, 490), 90)
    r2 = robot((400, 490), 90)
    r1.point_scanner(180, 10)
    r1.scan(r2.position)
    assert r1.scanned() == [r2.position]


def test_3():
    """
    Test 3: r2 está a 100m de distancia de r1, en el
            eje x e y, y en el margen inf der.
        Ejemplo:
            r1
                r2
    """
    r1 = robot((500, 600), 90)
    r2 = robot((600, 500), 90)
    r1.point_scanner(315, 9)
    r1.scan(r2.position)
    assert r1.scanned() == [r2.position]


def test_4():
    """
    Test 4: r2 está a 100m de las posiciones x e y.
        Ejemplo:
                r2
            r1
    """
    r1 = robot((500, 500), 90)
    r2 = robot((600, 600), 90)
    r1.point_scanner(45, 9)
    r1.scan(r2.position)
    assert r1.scanned() == [r2.position]


def test_5():
    """
    Test 5: r2 está  a 100m de las posiciones x e y.
        Ejemplo:
                r1
            r2
    """
    r1 = robot((600, 600), 90)
    r2 = robot((500, 500), 90)
    r1.point_scanner(225, 9)
    r1.scan(r2.position)
    assert r1.scanned() == [r2.position]


def test_6():
    """
    Test 6: r2 está a más de 100m de distancia de r1, en el
            eje x e y, y en el margen inf der, por lo que con
            un rango de 10 en el escáner no llega a detectarlo.
        Ejemplo:
            r1
                r2
    """
    r1 = robot((500, 600), 90)
    r2 = robot((600, 500), 90)
    r1.point_scanner(315, 10)
    r1.scan(r2.position)
    assert r1.scanned() == []


def test_7():
    """
    Test 7: Trae la distancia mínima aunque dos robots estén en el rango.
    """
    r1 = robot((500, 600), 90)
    r2 = robot((600, 500), 90)
    r3 = robot((610, 500), 90)
    r1.point_scanner(315, 9)
    r1.scan(r2.position, r3.position)
    assert r1.scanned() == [r2.position]
