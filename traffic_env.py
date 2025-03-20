import os
import sys
import traci
import numpy as np
import cv2
from gym import Env
from gym.spaces import Box, Discrete

class TrafficEnvironment(Env):
    def __init__(self, gui=False):
        super().__init__()
        
        # SUMO Configuration
        self.gui = gui
        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit("Please declare environment variable 'SUMO_HOME'")
            
        # Define action and observation spaces
        self.action_space = Discrete(4)  # 4 possible phases for traffic signal
        self.observation_space = Box(low=0, high=255, shape=(84, 84, 1), dtype=np.uint8)
        
        # Traffic simulation parameters
        self.max_steps = 1000
        self.current_step = 0
        
    def reset(self):
        # Start SUMO simulation
        if self.gui:
            sumoBinary = 'sumo-gui'
        else:
            sumoBinary = 'sumo'
        
        sumoCmd = [sumoBinary, '-c', 'intersection.sumocfg',
                   '--no-step-log', '--no-warnings']
        
        traci.start(sumoCmd)
        self.current_step = 0
        
        return self._get_state()
    
    def step(self, action):
        # Execute action
        self._apply_action(action)
        
        # Simulate one step
        traci.simulationStep()
        
        # Get new state
        state = self._get_state()
        
        # Calculate reward
        reward = self._compute_reward()
        
        # Check if episode is done
        self.current_step += 1
        done = self.current_step >= self.max_steps
        
        if done:
            traci.close()
            
        return state, reward, done, {}
    
    def _get_state(self):
        # Get traffic image from SUMO
        screenshot = self._get_traffic_image()
        
        # Process image
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (84, 84))
        
        return np.expand_dims(resized, axis=-1)
    
    def _apply_action(self, action):
        # Define traffic light phases
        phases = [
            'GGrrGGrr',  # North-South Green
            'yyrryyrr',  # North-South Yellow
            'rrGGrrGG',  # East-West Green
            'rryyrryy'   # East-West Yellow
        ]
        
        # Set traffic light phase
        traci.trafficlight.setRedYellowGreenState('intersection', phases[action])
    
    def _compute_reward(self):
        # Calculate reward based on waiting time and queue length
        total_wait_time = 0
        total_queue_length = 0
        
        for edge_id in traci.edge.getIDList():
            total_wait_time += sum([traci.vehicle.getWaitingTime(veh) 
                                  for veh in traci.edge.getLastStepVehicleIDs(edge_id)])
            total_queue_length += traci.edge.getLastStepHaltingNumber(edge_id)
        
        # Negative reward for waiting time and queue length
        reward = -(total_wait_time + total_queue_length)
        
        return reward
    
    def _get_traffic_image(self):
        # This is a placeholder for getting actual traffic camera image
        # In real implementation, this would get image from camera or SUMO GUI
        return np.zeros((480, 640, 3), dtype=np.uint8)
    
    def close(self):
        traci.close()