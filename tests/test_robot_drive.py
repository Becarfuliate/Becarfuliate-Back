from routers.robot.robot_class import robot


def test1():
    new = robot()
    new.drive(50,70)
    assert new.required_direction == 50 and new.required_velocity == 70

def test2():
    new = robot()
    new.drive(51,71)
    assert new.required_direction != 50 and new.required_velocity != 70
