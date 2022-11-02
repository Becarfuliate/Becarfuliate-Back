import pytest
from routers.robot.robot_class import robot

def test_1():
    robot1 = robot((0,0),0)
    robot1.required_direction = 90
    robot1.required_velocity = 100
    robot1._move()
    assert robot1.current_position == (0,50)

def test_polartorect1():
    robot1 = robot((0,0),0)
    res = robot1.polar_to_rect(270,100,(0,0))
    assert res == (0,0)

def test_polartorect2():
    robot1 = robot((0,0),0)
    res = robot1.polar_to_rect(180+45,1000,(200,400))
    assert res == (0,200)

def test_polartorect3():
    robot1 = robot((0,0),0)
    res = robot1.polar_to_rect(179,200,(100,500))
    assert res == (0,501,5)

def test_polartorect4():
    robot1 = robot((0,0),0)
    res = robot1.polar_to_rect(20,1000,(100,500))
    assert res == (0,501,5)

def test_blockdrirection1():
    robot1 = robot((0,0),0)
    res = robot1.block_direction(90,50,270)
    assert res == 270

def test_blockdrirection2():
    robot1 = robot((0,0),0)
    res = robot1.block_direction(90,51,270)
    assert res == 180
