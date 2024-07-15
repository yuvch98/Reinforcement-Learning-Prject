#e environment.py

import numpy as np
from agent import Agent
from policeman import Policeman
import constants as Const


class Environment:
    def __init__(self,grid_x, grid_y):
        self.grid = np.zeros((grid_x, grid_y))
        self.values = np.zeros((grid_x, grid_y))
        self.policies = np.zeros((grid_x, grid_y))
        self.terminal_states = set()
        self.rewards = {}
        self.transition_proba = np.ones((grid_x, grid_y, 4))*0.25 # for equal proba

