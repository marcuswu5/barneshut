from barnes_hut.tree import Tree
from particle import Particle


def kick_half(particles : list[Particle], dt : float):
    for p in particles:
        p.kick(dt * 0.5)

def drift(particles : list[Particle], dt : float):
    for p in particles:
        p.drift(dt)

