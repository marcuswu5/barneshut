from curses.ascii import SI
from node import Node, Boundary
from particle import Particle
from utils import Vector as V, getCenterOfMass
import config

SIZE = config.MAX_SIZE

class Tree:
    def __init__(self) -> None:
        self.root : Node = Node(V(), 0.0, Boundary(SIZE / 2,SIZE / 2,SIZE,SIZE))

    def split_node(self, p1 : Particle, p2 : Particle, n : Node):
        #p1 and p2 should be in bounds
        xmid = (p1.position.x + p2.position.x) / 2
        ymid = (p1.position.y + p2.position.y) / 2
        b = n.boundary
        for i in range(2):
            for j in range(2):
                newBound = Boundary(b.x + xmid * i, b.y * ymid * j,b.width / 2, b.height / 2)
                n.children.append(Node(V(),0.0,newBound))

    def insert_particle(self, p : Particle):
        cNode = self.root
        
        #Traverse the tree
        while len(cNode.children) > 0:
            cNode.center_of_mass = getCenterOfMass(cNode.total_mass,cNode.center_of_mass,p.mass,p.position)
            cNode.total_mass += p.mass

            for child in cNode.children:
                if child.boundary.inBounds(p.position):
                    cNode = child
                    break
        
        if not cNode.particle:
            cNode.particle = p
        else:
            self.split_node(cNode.particle,p,cNode)
            for particle in [p,cNode.particle]:
                for child in cNode.children:
                    if child.boundary.inBounds(particle.position):
                        cNode.center_of_mass = getCenterOfMass(cNode.total_mass,cNode.center_of_mass,particle.mass,particle.position)
                        cNode.total_mass += p.mass
                        cNode.particle = particle
                    break
            cNode.particle = None
    
    def create_tree(self, particles : list[Particle]):
        for particle in particles:
            if self.root.boundary.inBounds(particle.position):
                self.insert_particle(particle)
            else:
                raise Exception("Error creating tree: Particle outside of valid bounds")

