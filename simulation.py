from barnes_hut.tree import Tree
from particle import Particle
import integrator
import config
from visualizer import visualize

class Simulation:
    def __init__(self, particles, dt, theta = config.THETA) -> None:
        self.tree : Tree
        self.particles : list[Particle] = particles
        self.time = 0.0
        self.dt = dt
        self.theta = theta

    def update_accelerations(self):
        for p in self.particles:
            p.acceleration = self.tree.compute_acceleration(p,self.theta)
            

    def step(self):
        dt = self.dt

        #Kick and Drift
        integrator.kick_half(self.particles, dt)
        integrator.drift(self.particles, dt)

        #Rebuild Tree and compute accelerations
        tree = Tree()
        for p in self.particles:
            tree.insert_particle(p)
        self.update_accelerations()


        #Finish Kick
        integrator.kick_half(self.particles, dt)

        self.time += dt

    def run_simulation(self, num_steps, should_visualize=False):
        for step in range(num_steps):
            self.step()
            if should_visualize:
                visualize(self.particles, self.time)