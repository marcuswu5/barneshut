from dataclasses import dataclass
from utils import Vector, vectorAdd, vectorScale

@dataclass
class Particle:
    id: int
    position: Vector
    velocity: Vector
    acceleration: Vector
    mass: float

    def add_force(self, force : Vector):
        self.acceleration = Vector(force.x / self.mass, force.y / self.mass)

    def kick(self, dt : float):
        self.velocity = vectorAdd(self.velocity,vectorScale(self.acceleration, dt))
    
    def drift(self, dt : float):
        self.position = vectorAdd(self.position, vectorScale(self.velocity,dt))