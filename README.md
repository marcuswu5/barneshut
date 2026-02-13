# Barnes-Hut N-Body Simulation

This project simulates and visualizes the gravitational interaction of thousands of particles using the Barnes-Hut algorithm for efficient force calculation.

## Features
- **Barnes-Hut Tree**: Efficient O(N log N) force calculation for large N-body systems
- **Spiral Galaxy Generator**: Particles initialized in a spiral galaxy pattern
- **Real-Time Visualization**: Animated 2D plot with color-coded particle speeds
- **GIF Export**: Save simulation as an animated GIF (no ffmpeg required)
- **Progress Bars**: tqdm progress bars for simulation and GIF export

## Requirements
- Python 3.8+
- numpy
- matplotlib
- tqdm
- Pillow

## Usage
1. Install dependencies:
   ```bash
   pip install numpy matplotlib tqdm pillow
   ```
2. Run the simulation:
   ```bash
   python main.py
   ```
   - A window will open showing the live simulation.
   - A GIF will be saved as `simulation.gif` in the project folder.

## Customization
- Edit `main.py` to change the number of particles, simulation steps, or initial distribution.
- The color of each particle reflects its speed relative to the map size.
- To generate a video instead of a GIF, install ffmpeg and use `save_simulation_video` (see `visualizer.py`).

## Files
- `main.py` - Entry point, simulation setup, and visualization
- `simulation.py` - Simulation loop and time integration
- `barnes_hut/tree.py` - Barnes-Hut tree and force calculation
- `particle.py`, `utils.py` - Particle and vector math
- `visualizer.py` - Real-time and GIF visualization

## Example Output
![Spiral Galaxy Example](example.gif)

---
Created with ❤️ using Python and matplotlib.
