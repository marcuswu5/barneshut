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
        self.time_text = self.ax.text(0.02, 0.95, '', transform=self.ax.transAxes, 
                                      fontsize=12, verticalalignment='top',
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
        
        # Update scatter plot
        self.scatter.set_offsets(positions)
        
        # Color particles by speed for visual interest
        speeds = np.array([np.sqrt(p.velocity.x**2 + p.velocity.y**2) for p in particles])
        speeds = np.clip(speeds, 0, np.max(speeds) if len(speeds) > 0 else 1)
        self.scatter.set_array(speeds)
        
        # Update text information
        self.time_text.set_text(f'Time: {time:.2f}')
        self.particle_count_text.set_text(f'Particles: {len(particles)}')
        
        # Draw trails
        self.ax.clear()
        self.ax.set_xlim(-self.max_size / 2, self.max_size / 2)
        self.ax.set_ylim(-self.max_size / 2, self.max_size / 2)
        self.ax.set_aspect('equal')
        self.ax.set_xlabel('X Position')
        self.ax.set_ylabel('Y Position')
        
        # Draw particle trails
        for p_id, trail in self.particle_trails.items():
            if len(trail) > 1:
                trail_array = np.array(list(trail))
                self.ax.plot(trail_array[:, 0], trail_array[:, 1], 'cyan', alpha=0.3, linewidth=0.5)
        
        # Redraw scatter plot
        self.scatter = self.ax.scatter(positions[:, 0], positions[:, 1], 
                                      s=30, c=speeds, cmap='hot', alpha=0.7, 
                                      edgecolors='white', linewidth=0.5)
        
        # Add colorbar for speed
        if len(particles) > 0:
            cbar = plt.colorbar(self.scatter, ax=self.ax, label='Speed')
        
        # Redraw text
        self.time_text = self.ax.text(0.02, 0.95, f'Time: {time:.2f}', 
                                      transform=self.ax.transAxes, fontsize=12,
                                      verticalalignment='top',
                                      bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        self.particle_count_text = self.ax.text(0.02, 0.90, f'Particles: {len(particles)}',
                                               transform=self.ax.transAxes, fontsize=12,
                                               verticalalignment='top',
                                               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
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
    plt.pause(0.001)  # Small pause to allow rendering


def create_visualizer(max_size=config.MAX_SIZE):
    """
    Create and return a ParticleVisualizer instance.
    
    Args:
        max_size: The size of the simulation space
    
    Returns:
        ParticleVisualizer instance
    """
    return ParticleVisualizer(max_size=max_size)
