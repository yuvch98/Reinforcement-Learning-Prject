import pygame
import numpy as np

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define the size of the grid and cells
CELL_SIZE = 40

def draw_grid(screen, grid_size):
    for i in range(grid_size):
        for j in range(grid_size):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)

def draw_action(screen, i, j, action):
    if action == 'U':
        start_pos = (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2)
        end_pos = (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE)
    elif action == 'D':
        start_pos = (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2)
        end_pos = (j * CELL_SIZE + CELL_SIZE // 2, (i + 1) * CELL_SIZE)
    elif action == 'L':
        start_pos = (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2)
        end_pos = (j * CELL_SIZE, i * CELL_SIZE + CELL_SIZE // 2)
    elif action == 'R':
        start_pos = (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2)
        end_pos = ((j + 1) * CELL_SIZE, i * CELL_SIZE + CELL_SIZE // 2)
    pygame.draw.line(screen, RED, start_pos, end_pos, 2)

def main(game_info):
    grid_size = game_info['grid_size']
    policy = game_info['policy']
    pygame.init()
    screen = pygame.display.set_mode((grid_size * CELL_SIZE, grid_size * CELL_SIZE))
    pygame.display.set_caption("Policy Visualization")
    clock = pygame.time.Clock()
    draw_grid(screen, grid_size)
    pygame.display.flip()
    # Set up a timer event to trigger every second
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    policy_items = list(policy.items())
    current_index = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                if current_index < len(policy_items):
                    (i, j), action = policy_items[current_index]
                    draw_action(screen, i, j, action)
                    pygame.display.flip()
                    current_index += 1
        clock.tick(30)
    pygame.quit()
