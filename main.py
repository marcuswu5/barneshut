import random
from particle import Particle
from simulation import Simulation
from utils import Vector
import config
from visualizer import create_visualizer, visualize, save_simulation_gif
from tqdm import tqdm
import numpy as np


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
        velocity = Vector()
        
        # Initialize acceleration to zero
        acceleration = Vector(0, 0)
        
        # Random mass
        mass = random.uniform(100, 3000)
        
        particles.append(Particle(
            id=i,
            position=position,
            velocity=velocity,
            acceleration=acceleration,
            mass=mass
        ))
    
    return particles


def create_spiral_particles(num_particles):
    """
    Create a spiral-shaped distribution of particles.
    """
    particles = []
    arms = 2  # Number of spiral arms
    spread = 0.2  # Spread of the spiral
    for i in range(num_particles):
        angle = np.random.uniform(0, 2 * np.pi)
        radius = np.random.normal(loc=0, scale=config.MAX_SIZE / 6)
        arm_offset = (i % arms) * np.pi / arms
        spiral_angle = angle + spread * radius + arm_offset
        x = radius * np.cos(spiral_angle)
        y = radius * np.sin(spiral_angle)
        position = Vector(x, y)
        # Tangential velocity for spiral motion
        v_mag = 40 + np.random.uniform(-5, 5)
        vx = -v_mag * np.sin(spiral_angle)
        vy = v_mag * np.cos(spiral_angle)
        velocity = Vector(vx, vy)
        acceleration = Vector(0, 0)
        mass = np.random.normal(1000,300)
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
    # Create spiral particles
    particles = create_random_particles(config.NUM_PARTICLES)

    sun = Particle(0,Vector(),Vector(),Vector(),100000000)

    particles.append(sun)

    # Create simulation
    sim = Simulation(particles, config.DT, config.THETA)
    
    # Create visualizer
    visualizer = create_visualizer(config.MAX_SIZE)
    
    # Custom visualization function for the simulation
    def vis_callback(p, t):
        visualizer.update_frame(p, t)
    
    print(f"Starting simulation with {len(particles)} particles...")
    
    # Reset simulation time to zero before starting visualization
    sim.time = 0.0

    # Run simulation with progress bar
    for step in tqdm(range(100), desc="Simulation Progress"):
        sim.step()
        if step % 5 == 0:  # Visualize every 5 steps instead of 10
            vis_callback(sim.particles, sim.time)
    
    # Save the simulation as a GIF (does not require ffmpeg)
    save_simulation_gif(sim, filename="simulation.gif", num_steps=1000, interval=1)
    visualizer.show()


if __name__ == "__main__":
    main()
