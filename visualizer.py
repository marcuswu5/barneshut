def save_simulation_gif(simulation, filename="simulation.gif", num_steps=100, interval=50, dpi=150):
    """
    Save the simulation as a GIF using matplotlib's PillowWriter.
    Args:
        simulation: Simulation object (must have .particles, .step(), .time)
        filename: Output GIF filename (e.g., 'simulation.gif')
        num_steps: Number of simulation steps to record
        interval: Delay between frames in ms
        dpi: GIF resolution
    """
    from matplotlib.animation import PillowWriter
    from tqdm import tqdm
    visualizer = ParticleVisualizer()
    fig = visualizer.fig
    def update(frame):
        simulation.step()
        visualizer.update_frame(simulation.particles, simulation.time)
        return visualizer.scatter, visualizer.time_text, visualizer.particle_count_text

    writer = PillowWriter(fps=1000//interval)
    # Wrap frames in tqdm for progress bar
    anim = animation.FuncAnimation(fig, update, frames=tqdm(range(num_steps), desc="Saving GIF frames"), blit=False, interval=interval)
    anim.save(filename, writer=writer, dpi=dpi)
    print(f"GIF saved to {filename}")

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import numpy as np
from particle import Particle
from collections import deque
import config


class ParticleVisualizer:
    """Real-time visualizer for the Barnes-Hut N-body simulation."""
    
    def __init__(self, max_size=config.MAX_SIZE, trail_length=50):
        """
        Initialize the visualizer.
        
        Args:
            max_size: The size of the simulation space
            trail_length: Number of previous positions to show for each particle
        """
        self.max_size = max_size
        self.trail_length = trail_length
        self.particle_trails = {}  # Store position history for each particle
        
        # Create figure and axis
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.ax.set_xlim(-max_size / 2, max_size / 2)
        self.ax.set_ylim(-max_size / 2, max_size / 2)
        self.ax.set_aspect('equal')
        self.ax.set_xlabel('X Position')
        self.ax.set_ylabel('Y Position')
        
        # Initialize plot elements
        self.scatter = self.ax.scatter([], [], s=30, c='cyan', alpha=0.7, edgecolors='white', linewidth=0.5)
        self.time_text = self.ax.text(0.98, 0.95, '', transform=self.ax.transAxes, 
                                      fontsize=12, verticalalignment='top', horizontalalignment='right',
                                      bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        self.particle_count_text = self.ax.text(0.02, 0.90, '', transform=self.ax.transAxes,
                                               fontsize=12, verticalalignment='top',
                                               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # Trail lines for each particle
        self.trail_lines = {}
        
    def update_frame(self, particles, time):
        """
        Update the visualization with current particle positions.
        
        Args:
            particles: List of Particle objects
            time: Current simulation time
        """
        if not particles:
            return
        
        # Update particle trails
        for p in particles:
            if p.id not in self.particle_trails:
                self.particle_trails[p.id] = deque(maxlen=self.trail_length)
            
            self.particle_trails[p.id].append((p.position.x, p.position.y))
        
        # Extract current positions
        positions = np.array([(p.position.x, p.position.y) for p in particles])
        
        # Color particles by normalized speed (relative to map size)
        speeds = np.array([np.sqrt(p.velocity.x**2 + p.velocity.y**2) for p in particles])
        max_speed = self.max_size * 10000  # Extend range: treat map size per step as 'max' speed
        norm_speeds = np.clip(speeds / max_speed, 0, 1)
        self.scatter.set_offsets(positions)
        self.scatter.set_array(norm_speeds)
        
        # Update text information only (do not recreate text objects)
        self.time_text.set_text(f'Time: {time:.2f}')
        self.particle_count_text.set_text(f'Particles: {len(particles)}')
        self.fig.canvas.draw_idle()
    
    def show(self):
        """Display the visualization."""
        plt.show()


def visualize(particles, time, visualizer=None):
    """
    Function called by the simulation to update the visualization.
    
    Args:
        particles: List of Particle objects
        time: Current simulation time
        visualizer: ParticleVisualizer instance (initialized on first call)
    """
    if visualizer is None:
        visualizer = ParticleVisualizer()
        visualize.visualizer = visualizer
    else:
        visualizer = visualize.visualizer
    
    visualizer.update_frame(particles, time)
    plt.pause(0.1)  # Increased pause to 100ms to see animation clearly


def create_visualizer(max_size=config.MAX_SIZE):
    """
    Create and return a ParticleVisualizer instance.
    
    Args:
        max_size: The size of the simulation space
    
    Returns:
        ParticleVisualizer instance
    """
    return ParticleVisualizer(max_size=max_size)
