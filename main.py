import random
from particle import Particle
from simulation import Simulation
from utils import Vector
import config
from visualizer import create_visualizer, visualize


def create_random_particles(num_particles):
    """
    Create a list of random particles for the simulation.
    
    Args:
        num_particles: Number of particles to create
    
    Returns:
        List of Particle objects
    """
    particles = []
    for i in range(num_particles):
        # Random position within the simulation space
        x = random.uniform(-config.MAX_SIZE / 2, config.MAX_SIZE / 2)
        y = random.uniform(-config.MAX_SIZE / 2, config.MAX_SIZE / 2)
        position = Vector(x, y)
        
        # Small random velocities
        vx = random.uniform(-10, 10)
        vy = random.uniform(-10, 10)
        velocity = Vector(vx, vy)
        
        # Initialize acceleration to zero
        acceleration = Vector(0, 0)
        
        # Random mass
        mass = random.uniform(1, 10)
        
        particles.append(Particle(
            id=i,
            position=position,
            velocity=velocity,
            acceleration=acceleration,
            mass=mass
        ))
    
    return particles


def main():
    """Main simulation runner with visualization."""
    # Create particles
    particles = create_random_particles(config.NUM_PARTICLES)
    
    # Create simulation
    sim = Simulation(particles, config.DT, config.THETA)
    
    # Create visualizer
    visualizer = create_visualizer(config.MAX_SIZE)
    
    # Custom visualization function for the simulation
    def vis_callback(p, t):
        visualizer.update_frame(p, t)
    
    print(f"Starting simulation with {len(particles)} particles...")
    
    # Run simulation
    try:
        for step in range(1000):
            sim.step()
            if step % 10 == 0:
                print(f"Step: {step}, Time: {sim.time:.2f}")
                vis_callback(sim.particles, sim.time)
    except KeyboardInterrupt:
        print("Simulation interrupted by user.")
    finally:
        visualizer.show()


if __name__ == "__main__":
    main()
