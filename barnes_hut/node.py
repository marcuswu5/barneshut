from dataclasses import dataclass, field
from utils import Vector
from particle import Particle

@dataclass
class Boundary:
    x: float
    y: float
    width: float
    height: float

    def inBounds(self, coords : Vector):
        return ((coords.x >= self.x and coords.x <= self.x + self.width) and 
                coords.y >= self.y and coords.y <= self.y + self.height)
@dataclass
class Node:
    center_of_mass: Vector
    total_mass: float
    boundary: Boundary
    children: list["Node"] = field(default_factory = list)
    particle: Particle | None = None
