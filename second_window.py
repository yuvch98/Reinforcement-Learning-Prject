# second_window.py

import constants as const
import pygame


class grid:  # TODO - Generate a grid so we can pick the cell we want to be the prize
    pass  # TODO -


def draw_grid(screen, grid_x, grid_y, cell_size) -> None:
    for row in range(grid_x):
        for col in range(grid_y):
            rect = pygame.Rect(col * cell_size, 250 + row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, const.GRID_COLOR, rect, 1)
            if col % 2 == 0 and row % 2 == 0:
                pygame.draw.rect(screen, const.CELL_EVEN_COLOR, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
            elif col % 2 == 1 and row % 2 == 0:
                pygame.draw.rect(screen, const.CELL_ODD_COLOR, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
            elif col % 2 == 0 and row % 2 == 1:
                pygame.draw.rect(screen, const.CELL_ODD_COLOR, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
            else:
                pygame.draw.rect(screen, const.CELL_EVEN_COLOR, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)


def main(information):
    screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    pygame.display.set_caption("Grid Input Interface")
    pygame.init()
    clock = pygame.time.Clock()
    running = True
    while running:
        # Any event that is happening should be mentioned in this for loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(const.BG_COLOR)
        # label_surface = const.FONT.render("Click where you want to put a wall", True, const.TEXT_COLOR)
        # screen.blit(label_surface, (300,300))
        cell_size = min(const.SCREEN_WIDTH // int(information['grid_size']), (const.SCREEN_HEIGHT - 250) // int(information['grid_size']))
        draw_grid(screen, int(information['grid_size']), int(information['grid_size']), cell_size)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
