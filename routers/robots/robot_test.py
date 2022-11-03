class MotherClass:
    x = 5


class MyClass(MotherClass):
    y = MotherClass.x + 5
