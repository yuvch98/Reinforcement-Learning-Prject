# policeman.py

import random


class Policeman:
    def __init__(self, grid_size, negative=-2, with_walls=False):
        self.grid_size = grid_size
        if with_walls:
            self.row = random.randint(3, self.grid_size-1)
        else:
            self.row = random.randint(1, self.grid_size - 1)
        self.col = random.randint(0, self.grid_size - 1)
        self.prev_direction = ''
        self.direction = random.choice(['U', 'D'])
        self.reward = max(negative, 0)

    def get_pos(self):
        return self.row, self.col

    def move(self):
        self.prev_direction = self.direction
        if self.prev_direction == 'U':
            if self.row - 1 >= 0:
                self.row -= 1
                self.direction = 'U'
            else:
                self.row += 1
                self.direction = 'D'
        if self.prev_direction == 'D':
            if self.row + 1 <= self.grid_size - 1:
                self.row += 1
                self.direction = 'D'
            else:
                self.row -= 1
                self.direction = 'U'

    def reset_police(self):
        while True:
            self.row = random.randint(1, self.grid_size-1)
            self.col = random.randint(0, self.grid_size-1)
            self.direction = random.choice(['U', 'D'])
            state = (self.row, self.col)
            if not state == (0, 0):
                break
