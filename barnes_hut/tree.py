from barnes_hut.node import Node, Boundary
from particle import Particle, get_accel
from utils import Vector as V, getCenterOfMass, vectorAdd, vectorScale
import config

SIZE = config.MAX_SIZE

class Tree:
    def __init__(self) -> None:
        self.root : Node = Node(V(), 0.0, Boundary(-SIZE / 2, -SIZE / 2, SIZE, SIZE))

    def split_node(self, p1 : Particle, p2 : Particle, n : Node):
        #p1 and p2 should be in bounds
        b = n.boundary
        half_width = b.width / 2
        half_height = b.height / 2
        for i in range(2):
            for j in range(2):
                newBound = Boundary(b.x + i * half_width, b.y + j * half_height, half_width, half_height)
                n.children.append(Node(V(), 0.0, newBound))

    def insert_particle(self, p : Particle):
        cNode = self.root

        if not cNode.boundary.inBounds(p.position):
            return
        
        #Traverse the tree
        while len(cNode.children) > 0:
            cNode.center_of_mass = getCenterOfMass(cNode.total_mass, cNode.center_of_mass, p.mass, p.position)
            cNode.total_mass += p.mass

            found_child = False
            for child in cNode.children:
                if child.boundary.inBounds(p.position):
                    cNode = child
                    found_child = True
                    break
            
            if not found_child:
                raise Exception(f"Particle at ({p.position.x}, {p.position.y}) not found in any child boundary")
        
        if not cNode.particle:
            cNode.particle = p
            cNode.total_mass = p.mass
            cNode.center_of_mass = p.position
        else:
            old_particle = cNode.particle
            self.split_node(old_particle, p, cNode)
            cNode.particle = None
            for particle in [old_particle, p]:
                for child in cNode.children:
                    if child.boundary.inBounds(particle.position):
                        self.insert_particle(particle)
                        break
    
    def create_tree(self, particles : list[Particle]):
        for particle in particles:
            if self.root.boundary.inBounds(particle.position):
                self.insert_particle(particle)
            else:
                raise Exception("Error creating tree: Particle outside of valid bounds")

    def compute_acceleration(self, p : Particle, theta = config.THETA):
        return compute_acceleration(self.root, p, theta)

def compute_acceleration(node : Node, p : Particle, theta : float):
    if not node:
        raise Exception("Error, accessed empty node while computing acceleration")
    if len(node.children) == 0:
        if node.particle:
            return get_accel(p.position,p.mass,node.particle.position,node.particle.mass)
        else:
            return V()
        
    r = vectorAdd(node.center_of_mass, vectorScale(p.position,-1))
    d = r.magnitude()
    s = node.boundary.width

    if s/d < config.THETA:
        return get_accel(p.position,p.mass,node.center_of_mass, node.total_mass)
    else:
        a = V()
        for child in node.children:
            a = vectorAdd(a,compute_acceleration(child, p, theta))
        return a
    