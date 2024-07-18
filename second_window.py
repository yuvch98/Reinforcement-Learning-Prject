import constants as const
import pygame
from button import Button
from input_box import InputBox

pygame.init()
FONT = pygame.font.Font(None, 22)


def draw_grid(screen, grid_x, grid_y, cell_size, selected_cells, slippery_cells) -> None:
    for row in range(grid_x):
        for col in range(grid_y):
            rect = pygame.Rect(col * cell_size, 250 + row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, const.GRID_COLOR, rect, 1)
            if (row, col) in selected_cells:
                reward = selected_cells[(row, col)]
                color = const.POSITIVE_REWARD_COLOR if reward > 0 else const.NEGATIVE_REWARD_COLOR
                pygame.draw.rect(screen, color, rect)  # Color based on reward value
            elif (row, col) in slippery_cells:
                pygame.draw.rect(screen, const.SLIPPERY_COLOR, rect)  # Aqua color for slippery cells
            elif col % 2 == 0 and row % 2 == 0:
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


def draw_label(screen, text, font, color, x, y):
    label_surface = font.render(text, True, color)
    screen.blit(label_surface, (x, y))


def main(information):
    screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    pygame.display.set_caption("Grid Input Interface")
    clock = pygame.time.Clock()
    running = True
    selected_cells = {}  # Dictionary to store selected cells and their rewards
    slippery_cells = set()  # Set to store slippery cells

    # Font for the label
    font = pygame.font.SysFont(None, 36)
    label_text = "Click cells to toggle glow and set reward"

    # Button setup
    continue_button = Button(600, 10, 150, 40, "Continue")
    finish_button = Button(600, 10, 150, 40, "Finish")
    save_button = Button(10, 100, 80, 30, "Save")

    # Input box for reward
    reward_input_active = False
    reward_input_box = InputBox(10, 60, 140, 32, '')

    continue_clicked = False
    finish_clicked = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not continue_clicked:
                result = continue_button.handle_event(event)
                if result == "Continue":
                    continue_clicked = True
                    label_text = "Click on a cell for slippery cell"
            else:
                result = finish_button.handle_event(event)
                if result == "Finish":
                    # Handle the finish button click here
                    running = False  # For now, just exit the loop
                    information['rewards'] = selected_cells
                    information['slippery'] = slippery_cells

            if reward_input_active:
                reward_input_box.handle_event(event)
                save_result = save_button.handle_event(event)
                if save_result == "Save" or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    try:
                        reward = float(reward_input_box.text)
                        selected_cells[reward_input_active] = reward
                        reward_input_active = False
                        reward_input_box.text = ''  # Clear the input box
                    except ValueError:
                        print("Invalid reward input")
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = x // cell_size
                    row = (y - 250) // cell_size
                    if 0 <= col < int(information['grid_size']) and 250 <= y < 250 + int(
                            information['grid_size']) * cell_size:
                        if continue_clicked:
                            if (row, col) in slippery_cells:
                                slippery_cells.remove((row, col))
                            else:
                                slippery_cells.add((row, col))
                        else:
                            if (row, col) in selected_cells:
                                del selected_cells[(row, col)]
                            else:
                                reward_input_active = (row, col)

        screen.fill(const.BG_COLOR)
        cell_size = min(const.SCREEN_WIDTH // int(information['grid_size']),
                        (const.SCREEN_HEIGHT - 250) // int(information['grid_size']))
        draw_label(screen, label_text, font, const.TEXT_COLOR, 10, 10)

        if not continue_clicked:
            continue_button.draw(screen)
        else:
            finish_button.draw(screen)


        draw_grid(screen, int(information['grid_size']), int(information['grid_size']), cell_size, selected_cells,
                  slippery_cells)

        if reward_input_active and not continue_clicked:
            draw_label(screen, "Press Enter to save reward:", font, const.TEXT_COLOR, 10, 30)
            reward_input_box.draw(screen)
            save_button.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    return information
