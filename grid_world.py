import numpy as np
from policeman import Policeman

ACTION_SPACE = ('U', 'D', 'L', 'R')


class Grid:
    def __init__(self, rows, cols, start, rewards, slippery, q={}):
        self.rows = rows
        self.cols = cols
        self.start = start
        self.i = start[0]
        self.j = start[1]
        self.rewards = rewards
        self.slippery = slippery
        self.actions = self.generate_actions()
        self.policeman = Policeman(self.rows)
        self.q = q

    def generate_actions(self):
        actions = {}
        for i in range(self.rows):
            for j in range(self.cols):
                if (i, j) not in self.rewards.keys():
                    action_list = []
                    if i > 0:
                        action_list.append('U')
                    if i < self.rows - 1:
                        action_list.append('D')
                    if j > 0:
                        action_list.append('L')
                    if j < self.cols - 1:
                        action_list.append('R')
                    if action_list:
                        actions[(i, j)] = tuple(action_list)
        return actions

    def current_state(self):
        return self.i, self.j

    def reset(self):
        self.i = self.start[0]
        self.j = self.start[1]
        return self.i, self.j

    def check_next_state(self, a):

        """
        this function is to check if policeman in next state
        if he is, returns true. else - returns false
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
        if self.policeman.get_pos() == (i, j):
            return True
        else:
            return False

    def second_best(self, a, q):
        self.q = q
        new_dict = self.q[(self.i, self.j)].copy()
        new_dict.pop(a)
        max_value = max(new_dict.values())
        new_action = ''
        for item in new_dict.keys():
            if new_dict[item] == max_value:
                new_action = item
            else:
                continue
        return new_action

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
        """
            if cell is slippery:
                should be 50% to the designated action
            else: random move
        else:
        perform the action
        """
        if (self.i, self.j) in self.slippery:
            if np.random.rand() < 0.5:
                # Move to a random cell
                new_action = np.random.choice(self.actions[(self.i, self.j)])
                self.i, self.j = self._move(self.i, self.j, new_action)
            else:
                # Move according to the action
                self.i, self.j = self._move(self.i, self.j, action)
        elif self.check_next_state(action):
            #  find a different action that is okay to go to.
            new_action = self.second_best(action, q)
            self.i, self.j = self._move(self.i, self.j, new_action)
        else:  # no issue with moving to the next cell.
            self.i, self.j = self._move(self.i, self.j, action)
            # Returns the reward of the cell. If it doesn't exist, it should be 0
        return self.rewards.get((self.i, self.j), 0)

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
        return (self.i, self.j) not in self.actions  # if the agent in a finite state

    def all_states(self):
        return set(self.actions.keys()) | set(self.rewards.keys())


def standard_grid(n, rewards, slippery, q={}):
    g = Grid(n, n, start=(0, 0), rewards=rewards, slippery=slippery, q=q)
    return g
