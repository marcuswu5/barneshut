from dataclasses import dataclass
from utils import Vector, vectorAdd, vectorScale
from math import pow
import config

@dataclass
class Particle:
    id: int
    position: Vector
    velocity: Vector
    acceleration: Vector
    mass: float

    def kick(self, dt : float):
        self.velocity = vectorAdd(self.velocity,vectorScale(self.acceleration, dt))
    
    def drift(self, dt : float):
        self.position = vectorAdd(self.position, vectorScale(self.velocity,dt))

#Gravitational force on p1 from p2
def get_accel(p1,m1,p2,m2):
    displacement = vectorAdd(p2, vectorScale(p1,-1))
    denom = pow(pow(displacement.magnitude(),2) + pow(config.EPSILON,2),3.0/2.0)
    scalar = config.G * m2 / denom
    return vectorScale(displacement, scalar)