# policeman.py

import random


class Policeman:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.row = random.randint(1, grid_size - 1)
        self.col = random.randint(0, grid_size - 1)
        self.direction = random.choice(['U', 'D'])

    def get_pos(self):
        return self.row, self.col

    def move(self):
        self.direction = random.choice(['U', 'D'])
        if self.direction == 'U':
            if self.row - 1 >= 0:
                self.row -= 1
        elif self.direction == 'D':
            if self. row + 1 <= self.grid_size - 1:
                self.row += 1

    def reset_police(self):
        self.row = random.randint(1, self.grid_size-1)
        self.col = random.randint(0, self.grid_size-1)
