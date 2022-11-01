import pytest
from routers.robot.robot_class import robot

def test_1():
    robot1 = robot((0,0),0)
    robot1.required_direction = 90
    robot1.required_velocity = 100
    robot1._move()
    assert robot1.current_position == (0,100)