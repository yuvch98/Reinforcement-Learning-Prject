from policeman import Policeman
ACTION_SPACE = ('U', 'D', 'L', 'R')


class Grid:
    def __init__(self, rows, cols, start, rewards, slippery):
        self.rows = rows
        self.cols = cols
        self.start = start
        self.i = start[0]
        self.j = start[1]
        self.rewards = rewards
        self.slippery = slippery
        self.actions = self.generate_actions()
        self.policeman = Policeman(rows)

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

    def set_state(self, s):
        self.i = s[0]
        self.j = s[1]

    def current_state(self):
        return self.i, self.j

    def is_terminal(self, s):
        return s not in self.actions

    def reset(self):
        self.i = self.start[0]
        self.j = self.start[1]
        return self.i, self.j

    def get_next_state(self, s, a):
        i, j = s[0], s[1]
        if a in self.actions.get((i, j), []):
            if a == 'U':
                i -= 1
            elif a == 'D':
                i += 1
            elif a == 'R':
                j += 1
            elif a == 'L':
                j -= 1
        return i, j

    def move(self, action):
        # check if legal move first
        if action in self.actions[(self.i, self.j)]:
            if action == 'U':
                self.i -= 1
            elif action == 'D':
                self.i += 1
            elif action == 'R':
                self.j += 1
            elif action == 'L':
                self.j -= 1
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
        return (self.i, self.j) not in self.actions  # if the agent not in the finite state

    def all_states(self):
        return set(self.actions.keys()) | set(self.rewards.keys())


def standard_grid(n, rewards, slippery):
    g = Grid(n, n, start=(0, 0), rewards=rewards, slippery=slippery)
    return g
