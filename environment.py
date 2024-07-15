# environment.py
import numpy as np
from agent import Agent
from policeman import Policeman
import constants as Const

class Environment:
    def __init__(self, grid_x, grid_y):
        self.grid = np.zeros((grid_x, grid_y))
        self.values = np.zeros((grid_x, grid_y))
        self.policies = np.zeros((grid_x, grid_y))
        self.terminal_states = set()
        self.rewards = {}
        self.transition_proba = np.ones((grid_x, grid_y, 4)) * 0.25  # for equal proba
        self.agent = Agent()
        self.police = Policeman()
        self.agent_pos = [0, 0]
        self.police_pos = [5, 5]
        self.terminal_state = None
        self.slippery_cells = set()

    def set_terminal_state(self, x, y):
        self.terminal_state = (x, y)
        self.terminal_states.add((x, y))
        self.rewards[(x, y)] = 1.0

    def add_slippery_cell(self, x, y):
        self.slippery_cells.add((x, y))

    def reset(self):
        self.agent_pos = [0, 0]
        self.police_pos = [5, 5]

    def step(self, action):
        next_state = self.agent_pos.copy()
        if action == 0:  # Up
            next_state[1] = max(0, self.agent_pos[1] - 1)
        elif action == 1:  # Down
            next_state[1] = min(self.grid.shape[1] - 1, self.agent_pos[1] + 1)
        elif action == 2:  # Left
            next_state[0] = max(0, self.agent_pos[0] - 1)
        elif action == 3:  # Right
            next_state[0] = min(self.grid.shape[0] - 1, self.agent_pos[0] + 1)

        # Slippery cell check
        if tuple(next_state) in self.slippery_cells and np.random.rand() < 0.5:
            action = np.random.choice([0, 1, 2, 3])
            if action == 0:  # Up
                next_state[1] = max(0, self.agent_pos[1] - 1)
            elif action == 1:  # Down
                next_state[1] = min(self.grid.shape[1] - 1, self.agent_pos[1] + 1)
            elif action == 2:  # Left
                next_state[0] = max(0, self.agent_pos[0] - 1)
            elif action == 3:  # Right
                next_state[0] = min(self.grid.shape[0] - 1, self.agent_pos[0] + 1)

        reward = self.rewards.get(tuple(next_state), 0)
        done = (tuple(next_state) == self.terminal_state)

        # Update agent position
        self.agent_pos = next_state

        # Check for collision with police
        if self.agent_pos == self.police_pos:
            reward -= 1
            done = True

        return next_state, reward, done

    def move_police(self):
        if self.police.direction == "random":
            self.police_pos = [np.random.randint(0, self.grid.shape[0]), np.random.randint(0, self.grid.shape[1])]
        else:
            # Move up and down
            if self.police.direction == "up":
                self.police_pos[1] = max(0, self.police_pos[1] - 1)
                if self.police_pos[1] == 0:
                    self.police.direction = "down"
            else:
                self.police_pos[1] = min(self.grid.shape[1] - 1, self.police_pos[1] + 1)
                if self.police_pos[1] == self.grid.shape[1] - 1:
                    self.police.direction = "up"
