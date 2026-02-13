from barnes_hut.tree import Tree
from particle import Particle

class Simulation:
    def __init__(self) -> None:
        self.tree : Tree
        self.particles = list[Particle]