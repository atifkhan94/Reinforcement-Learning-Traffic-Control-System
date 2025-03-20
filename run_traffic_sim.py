import os
import sys

# Set SUMO_HOME environment variable
os.environ['SUMO_HOME'] = 'C:/Program Files (x86)/Eclipse/Sumo'

from traffic_env import TrafficEnvironment

def main():
    # Create environment with GUI enabled
    env = TrafficEnvironment(gui=True)
    
    # Reset environment to initialize simulation
    state = env.reset()
    
    # Run for a few steps to test
    for _ in range(100):
        action = env.action_space.sample()  # Random action
        state, reward, done, _ = env.step(action)
        
        if done:
            break
    
    # Close environment
    env.close()

if __name__ == '__main__':
    main()

os.environ['SUMO_HOME'] = 'C:\\Program Files (x86)\\Eclipse\\Sumo'