import numpy as np
from policeman import Policeman

ACTION_SPACE = ('U', 'D', 'L', 'R')


class Grid:
    def __init__(self, rows, cols, start, rewards, slippery, walls, coins, reward_per_coin, walls_to_remove, lever=None, q={}):
        self.rows = rows
        self.cols = cols
        self.start = start
        self.i = start[0]
        self.j = start[1]
        self.rewards = rewards
        self.slippery = slippery
        self.old_walls = walls.copy()
        self.walls = walls
        self.actions = self.generate_actions()
        self.policeman = Policeman(self.rows)
        self.q = q
        self.coins = coins
        self.reward_coin = reward_per_coin
        self.lever = lever
        self.walls_to_remove = walls_to_remove
        self.terminal_states = rewards
        self.lever_reward = 0
        self.visited_lever = False
        self.old_coins = coins.copy()

    def generate_actions(self):
        actions = {}
        for i in range(self.rows):
            for j in range(self.cols):
                if (i, j) not in self.rewards.keys() and (i, j) not in self.walls:
                    action_list = []
                    if i > 0 and (i - 1, j) not in self.walls:
                        action_list.append('U')
                    if i < self.rows - 1 and (i + 1, j) not in self.walls:
                        action_list.append('D')
                    if j > 0 and (i, j - 1) not in self.walls:
                        action_list.append('L')
                    if j < self.cols - 1 and (i, j + 1) not in self.walls:
                        action_list.append('R')
                    if action_list:
                        actions[(i, j)] = tuple(action_list)
        return actions

    def update_actions(self):
        self.actions = self.generate_actions()

    def current_state(self):
        return self.i, self.j

    def reset(self):
        self.i = self.start[0]
        self.j = self.start[1]
        self.walls = self.old_walls.copy()
        self.coins = self.old_coins.copy()
        self.actions = self.generate_actions()
        self.visited_lever = False
        return self.i, self.j

    def random_action(self):
        return np.random.choice(self.actions[(self.i, self.j)])

    def check_next_state(self, a) -> bool:
        """
        this function is to check if policeman in next state
        if policeman, returns True. else: False
        """
        i, j = self.current_state()
        if a == 'U' and i > 0:
            i -= 1
        if a == 'D' and i < self.rows - 1:
            i += 1
        if a == 'L' and j > 0:
            j -= 1
        if a == 'R' and j < self.cols - 1:
            j += 1
        # if (i, j) in self.rewards:
        #     return False
        if self.policeman.get_pos() == (i, j) or (i, j) in self.walls:
            return True
        else:
            return False

    def _move(self, i, j, a):
        if a == 'U' and i > 0:
            i -= 1
        elif a == 'D' and i < self.rows - 1:
            i += 1
        elif a == 'L' and j > 0:
            j -= 1
        elif a == 'R' and j < self.cols - 1:
            j += 1
        return i, j

    def move(self, action, q):
        r = 0
        # First, check if the current cell is slippery
        if (self.i, self.j) in self.slippery:
            if np.random.rand() < 0.5:
                # Move to a random adjacent cell
                action = self.random_action()
                self.i, self.j = self._move(self.i, self.j, action)
            else:
                # Move according to the intended action
                self.i, self.j = self._move(self.i, self.j, action)
        else:
            # checking if policeman in the next state
            if self.check_next_state(action):
                action = self.random_action()
                self.i, self.j = self._move(self.i, self.j, action)
            else:

                # Move according to the intended action
                self.i, self.j = self._move(self.i, self.j, action)

        # Check if the new cell is a wall
        if (self.i, self.j) in self.walls:
            print(f"Agent hit a wall at {(self.i, self.j)}")
            self.undo_move(action)

        # Check if the agent meets the policeman
        if (self.i, self.j) == self.policeman.get_pos():
            r += self.policeman.reward  # Apply penalty from the policeman
            print(f"Agent encountered policeman at {(self.i, self.j)}, reward: {r}")
            return r  # Terminate the episode

        # Check if the current cell is a coin cell
        if (self.i, self.j) in self.coins:
            r += self.reward_coin  # Get the reward of the coin
            self.coins.remove((self.i, self.j))  # Remove the coin
            return r
        # Check if the current cell is a lever
        if not self.visited_lever and self.lever is not None:
            if (self.i, self.j) == self.lever:
                for wall in self.walls_to_remove:
                    self.walls.remove(wall)  # Remove the specified walls
                self.update_actions()  # Update actions after removing walls
                r += self.lever_reward  # Lever might have a reward
                self.visited_lever = True
                return r
        # Add reward of the current cell
        r += self.rewards.get((self.i, self.j), 0)
        return r

    def undo_move(self, action):
        if action == 'U':
            self.i += 1
        elif action == 'D':
            self.i -= 1
        elif action == 'R':
            self.j -= 1
        elif action == 'L':
            self.j += 1
        assert self.current_state() in self.all_states(), "State after undo should be valid."

    def game_over(self):
        return (self.i, self.j) not in self.actions or (self.i, self.j) == self.policeman.get_pos()  # if the agent in a finite state

    def all_states(self):
        return set(self.actions.keys()) | set(self.rewards.keys()) | self.walls

    def print_values(self):
        print(f"actions: {self.actions}")
        print(f"q table: {self.q}")
        print(f"rewards: {self.rewards}")


def standard_grid(n, rewards, slippery, walls, coins, lever, reward_per_coin, walls_to_remove, q={}):
    g = Grid(n, n, start=(0, 0), rewards=rewards, slippery=slippery, walls=walls, coins=coins, q=q, lever=lever, reward_per_coin=reward_per_coin, walls_to_remove=walls_to_remove)
    return g
