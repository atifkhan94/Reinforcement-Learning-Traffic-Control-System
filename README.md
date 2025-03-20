# Reinforcement Learning Traffic Control System

This project implements a reinforcement learning-based traffic signal control system using SUMO (Simulation of Urban MObility) traffic simulator. The system uses computer vision and deep reinforcement learning techniques to optimize traffic flow at an intersection.

## Features

- Real-time traffic signal control using reinforcement learning
- Integration with SUMO traffic simulator
- OpenCV-based traffic state representation
- Customizable reward function based on waiting time and queue length
- Support for both GUI and non-GUI simulation modes

## Prerequisites

- Python 3.x
- SUMO (Simulation of Urban MObility)
- OpenCV
- NumPy
- Gym

## Installation

1. Install SUMO following the instructions at [SUMO Installation Guide](https://sumo.dlr.de/docs/Installing.html)

2. Set the SUMO_HOME environment variable:
   ```
   # Windows
   set SUMO_HOME=C:\Program Files (x86)\Eclipse\Sumo
   
   # Linux/Mac
   export SUMO_HOME=/path/to/sumo
   ```

3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

## Project Structure

- `traffic_env.py`: Main environment class implementing the Gym interface
- `run_traffic_sim.py`: Script to run the traffic simulation
- `intersection.sumocfg`: SUMO configuration file
- `intersection.net.xml`: SUMO network definition
- `intersection.rou.xml`: SUMO route definition

## Usage

1. Run the simulation:
   ```python
   python run_traffic_sim.py
   ```

2. The simulation will run for 100 steps with random actions to demonstrate the environment functionality.

## Environment Details

### State Space
- 84x84x1 grayscale image representing the traffic state

### Action Space
- 4 discrete actions representing different traffic light phases:
  - North-South Green
  - North-South Yellow
  - East-West Green
  - East-West Yellow

### Reward Function
- Negative reward based on:
  - Total waiting time of vehicles
  - Queue length at the intersection

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.