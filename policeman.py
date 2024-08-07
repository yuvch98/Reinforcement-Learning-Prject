import random


class Policeman:
    def __init__(self, grid_size, with_walls=False):
        """
        Initializes the Policeman object.

        Args:
            grid_size (int): The size of the grid.
            with_walls (bool, optional): Flag indicating if walls are present. Default is False.
        """
        self.grid_size = grid_size
        if with_walls:
            self.row = random.randint(3, self.grid_size - 1)
        else:
            self.row = random.randint(1, self.grid_size - 1)
        self.col = random.randint(0, self.grid_size - 1)
        self.prev_direction = ''
        self.direction = random.choice(['U', 'D'])
        self.reward = -10

    def get_pos(self):
        """
        Returns the current position of the policeman.

        Returns:
            tuple: Current position (row, col) of the policeman.
        """
        return self.row, self.col

    def move(self):
        """
        Moves the policeman in the current direction. If the policeman hits the grid boundary,
        it changes direction.
        """
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
        """
        Resets the policeman to a random position on the grid, ensuring the position is not (0, 0).
        """
        while True:
            self.row = random.randint(1, self.grid_size - 1)
            self.col = random.randint(0, self.grid_size - 1)
            self.direction = random.choice(['U', 'D'])
            state = (self.row, self.col)
            if not state == (0, 0):
                break
