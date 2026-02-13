from dataclasses import dataclass

@dataclass
class Vector:
    x: float = 0.0
    y: float = 0.0

def vectorScale(v : Vector, c : float):
    return Vector(v.x * c, v.y * c)

def vectorAdd(v1 : Vector, v2 : Vector):
    return Vector(v1.x + v2.x, v1.y + v2.y)

def getCenterOfMass(mass1 : float, coord1 : Vector, mass2 : float, coord2 : Vector):
    w1 = mass1 / (mass1 + mass2)
    w2 = mass2 / (mass1 + mass2)
    return vectorAdd(vectorScale(coord1, w1),vectorScale(coord2, w2))