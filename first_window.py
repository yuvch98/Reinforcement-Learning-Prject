#e first_window.py

import constants as const
import pygame
from button import Button
from input_box import InputBox
from combo_box import ComboBox
pygame.init()
import environment


# Initialize screen
screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
pygame.display.set_caption("Grid Input Interface")
# def draw_grid(screen, grid_x, grid_y, cell_size) -> None:
#     for row in range(grid_x):
#         for col in range(grid_y):
#             rect = pygame.Rect(col * cell_size, 250 + row * cell_size, cell_size, cell_size)
#             pygame.draw.rect(screen, const.GRID_COLOR, rect, 1)
#             if col % 2 == 0 and row % 2 == 0:
#                 pygame.draw.rect(screen, const.CELL_EVEN_COLOR, rect)
#                 pygame.draw.rect(screen, (0, 0, 0), rect, 1)
#             elif col % 2 == 1 and row % 2 == 0:
#                 pygame.draw.rect(screen, const.CELL_ODD_COLOR, rect)
#                 pygame.draw.rect(screen, (0, 0, 0), rect, 1)
#             elif col % 2 == 0 and row % 2 == 1:
#                 pygame.draw.rect(screen, const.CELL_ODD_COLOR, rect)
#                 pygame.draw.rect(screen, (0, 0, 0), rect, 1)
#             else:
#                 pygame.draw.rect(screen, const.CELL_EVEN_COLOR, rect)
#                 pygame.draw.rect(screen, (0, 0, 0), rect, 1)


def check_all_lines(input_boxes) -> bool:
    for key in input_boxes.keys():
        if key == "grid_size":
            if int(input_boxes[key].text) > 10 or int(input_boxes[key].text) < 1:
                print(f"Failure, {key} ,must be between 1 and 10")
                return True
        elif key == 'alpha' or key == 'gamma' or key == 'epsilon':
            if float(input_boxes[key].text) > 1 or float(input_boxes[key].text) < 0:
                print(f"Failure, {key} must be between 0 and 1")
                return True
        elif key == "num_episodes" or key == 'max_steps_per_episode' or key == 'training_phase' or key == 'play_phase':
            if int(input_boxes[key].text) < 0:
                print(f"Failure, {key} must be bigger than 0")
                return True
    return False


def main():
    information = {
        'grid_size': 5,
        'alpha': 0.1,
        'gamma': 0.9,
        'epsilon': 0.1,
        'episode': 100,
        'max_steps_per_episode': 50,
        'training_phase': 1000,
        'play_phase': 100,
    }
    running = True
    clock = pygame.time.Clock()
    algorithm = ""
    # Creating input boxes for all parameters
    input_boxes = {
        'grid_size' : InputBox(400, 20, 120, 32, '5'),
        'alpha' : InputBox(400, 60, 120, 32, '0.1'),
            'gamma' : InputBox(400, 100, 120, 32, '0.9'),
        'epsilon' : InputBox(400, 140, 120, 32, '0.1'),
        'max_steps_per_episode' : InputBox(400, 180, 120, 32, '50'),
    'episode' : InputBox(400, 220, 120, 32, '100'),
    'training_phase':InputBox(400, 260, 120, 32, '1000'),
    'play_phase' : InputBox(400, 300, 120, 32, '100'),
    }
    combo_box = ComboBox(400, 340, 120, 50, const.FONT, ['Q Learning', 'SARSA'])
    # Corresponding labels for the input boxes
    buttons = [
        Button(700, 320, 120, 50, 'Continue')
    ]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for box in input_boxes.values():
                box.handle_event(event)
            for button in buttons:
                algorithm = button.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if buttons[-1].rect.collidepoint(x, y):
                    print("Hello World !")
                    running = check_all_lines(input_boxes)
            combo_box.handle_event(event)
        screen.fill(const.BG_COLOR)

        # Draw labels and input boxes
        for i, box in enumerate(input_boxes.keys()):
            label_surface = const.FONT.render(box, True, const.TEXT_COLOR)
            screen.blit(label_surface, (input_boxes[box].rect.x - 200, input_boxes[box].rect.y + 5))
            input_boxes[box].draw(screen)
        algorithm_label = const.FONT.render('algorithm', True, const.TEXT_COLOR)
        screen.blit(algorithm_label, (200, 355))
        for button in buttons:
            button.draw(screen)

        combo_box.draw(screen)

        pygame.display.flip()
        clock.tick(30)
    print(information)
    pygame.quit()
    return information
