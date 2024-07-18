import constants as const
import pygame
from button import Button
from input_box import InputBox
from combo_box import ComboBox
import second_window  # Ensure this is your second window module


# Initialize Pygame
pygame.init()

# Font
FONT = pygame.font.Font(None, 22)

# Initialize screen
screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
pygame.display.set_caption("Input Information")

def check_all_lines(input_boxes) -> bool:
    try:
        for key in input_boxes.keys():
            if key == "grid_size":
                if int(input_boxes[key].text) > 10 or int(input_boxes[key].text) < 1:
                    print(f"Failure, {key} must be between 1 and 10")
                    return True
            elif key in ['alpha', 'gamma', 'epsilon']:
                if float(input_boxes[key].text) > 1 or float(input_boxes[key].text) < 0:
                    print(f"Failure, {key} must be between 0 and 1")
                    return True
            elif key in ["num_episodes", 'max_steps_per_episode', 'training_phase', 'play_phase']:
                if int(input_boxes[key].text) < 0:
                    print(f"Failure, {key} must be bigger than 0")
                    return True
    except ValueError as e:
        print(f"ValueError: {e}")
        return True
    return False

def main():
    information = {
        'grid_size': 5,
        'alpha': 0.1,
        'gamma': 0.9,
        'epsilon': 0.1,
        'max_steps_per_episode': 50,
        'training_phase': 1000,
        'play_phase': 100,
    }
    running = True
    clock = pygame.time.Clock()

    # Creating input boxes for all parameters
    input_boxes = {
        'grid_size': InputBox(400, 20, 120, 32, '5'),
        'alpha': InputBox(400, 60, 120, 32, '0.1'),
        'gamma': InputBox(400, 100, 120, 32, '0.9'),
        'epsilon': InputBox(400, 140, 120, 32, '0.1'),
        'max_steps_per_episode': InputBox(400, 180, 120, 32, '50'),
        'training_phase': InputBox(400, 220, 120, 32, '1000'),
        'play_phase': InputBox(400, 260, 120, 32, '100'),
    }
    combo_box = ComboBox(400, 300, 120, 50, FONT, ['Q_Learning', 'SARSA'])

    # Corresponding labels for the input boxes
    button = Button(700, 320, 120, 50, 'Continue')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for box in input_boxes.values():
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if button.rect.collidepoint(x, y):
                    if not check_all_lines(input_boxes):
                        information.update({key: box.text for key, box in input_boxes.items()})
                        information['algorithm'] = combo_box.selected_option
                        second_window.main(information)
                        running = False  # Ensure the loop terminates properly
            combo_box.handle_event(event)

        if not running:
            break  # Exit the loop if running is set to False

        screen.fill(const.BG_COLOR)

        # Draw labels and input boxes
        for i, box in enumerate(input_boxes.keys()):
            label_surface = FONT.render(box, True, const.TEXT_COLOR)
            screen.blit(label_surface, (input_boxes[box].rect.x - 200, input_boxes[box].rect.y + 5))
            input_boxes[box].draw(screen)

        algorithm_label = FONT.render('algorithm', True, const.TEXT_COLOR)
        screen.blit(algorithm_label, (200, 310))

        button.draw(screen)
        combo_box.draw(screen)

        pygame.display.flip()
        clock.tick(30)  # animation speed

    for key in input_boxes.keys():
        information[key] = input_boxes[key].text
    information['algorithm'] = combo_box.selected_option
    pygame.quit()
    return information
