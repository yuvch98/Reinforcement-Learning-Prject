#e first_window.py

import constants as const
import pygame
import pygame.locals as pl
from button import Button
from input_box import InputBox
pygame.init()



# Initialize screen
screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
pygame.display.set_caption("Grid Input Interface")




def reset_fields(input_boxes):
    for i, box in enumerate(input_boxes):
        if i < 2:  # grid_x and grid_y
            box.text = '5'
        else:
            box.text = ''
        box.txt_surface = const.FONT.render(box.text, True, const.TEXT_COLOR)



def draw_grid(screen, grid_x, grid_y, cell_size):
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


def main():
    clock = pygame.time.Clock()

    # Creating input boxes for all parameters
    input_boxes = [
        InputBox(200, 20, 120, 32, '5'),
        InputBox(450, 20, 120, 32, '5'),
        InputBox(200, 70, 120, 32, ''),
        InputBox(450, 70, 120, 32, ''),
        InputBox(200, 120, 120, 32, ''),
        InputBox(450, 120, 120, 32, ''),
        InputBox(200, 170, 120, 32, ''),
        InputBox(450, 170, 120, 32, ''),
    ]

    # Corresponding labels for the input boxes
    labels = [
        'Grid X:', 'Grid Y:',
        'delta:', 'gamma:',
        'epsilon:', 'epsiode:',
        'training phase:', 'play phase:'
    ]
    buttons = [
        Button(750, 20, 120, 50, 'Q Learning'),
        Button(750, 70, 120, 50, 'SARSA'),
        Button(750, 120, 120, 50, 'Reset', action=lambda: reset_fields(input_boxes)),
    ]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for box in input_boxes:
                box.handle_event(event)
            for button in buttons:
                button.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print(x,y)

        screen.fill(const.BG_COLOR)

        # Draw labels and input boxes
        for i, box in enumerate(input_boxes):
            label_surface = const.FONT.render(labels[i], True, const.TEXT_COLOR)
            screen.blit(label_surface, (box.rect.x - 110, box.rect.y + 5))
            box.draw(screen)

        for button in buttons:
            button.draw(screen)

        try:
            grid_x = int(input_boxes[0].text)
            grid_y = int(input_boxes[1].text)

            # Ensure values are between 1 and 10
            if 1 <= grid_x <= 10 and 1 <= grid_y <= 10:
                cell_size = min(const.SCREEN_WIDTH // grid_y, (const.SCREEN_HEIGHT - 250) // grid_x)
                draw_grid(screen, grid_x, grid_y, cell_size)
            else:
                error_surface = const.FONT.render("Values must be between 1 and 10", True, (255, 0, 0))
                screen.blit(error_surface, (const.SCREEN_WIDTH // 2 - error_surface.get_width() // 2, const.SCREEN_HEIGHT // 2))
        except ValueError:
            pass

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
