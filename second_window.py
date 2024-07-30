import constants as const
import pygame
from button import Button
from input_box import InputBox

pygame.init()
FONT = pygame.font.Font(None, 22)

def draw_grid(screen, grid_x, grid_y, cell_size, selected_cells, slippery_cells, coin_cells, lever_cell, wall_positions, walls_to_remove):
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
            elif (row, col) in coin_cells:
                coin_image = pygame.image.load("coin.png").convert_alpha()
                coin_image = pygame.transform.scale(coin_image, (cell_size, cell_size))
                screen.blit(coin_image, (col * cell_size, 250 + row * cell_size))
            elif lever_cell and (row, col) == lever_cell:
                lever_image = pygame.image.load("lever.png").convert_alpha()
                lever_image = pygame.transform.scale(lever_image, (cell_size, cell_size))
                screen.blit(lever_image, (col * cell_size, 250 + row * cell_size))
            elif (row, col) in walls_to_remove:
                remove_image = pygame.image.load("remove.png").convert_alpha()
                remove_image = pygame.transform.scale(remove_image, (cell_size, cell_size))
                screen.blit(remove_image, (col * cell_size, 250 + row * cell_size))
            elif (row, col) in wall_positions:
                wall_image = pygame.image.load("wall.png").convert_alpha()
                wall_image = pygame.transform.scale(wall_image, (cell_size, cell_size))
                screen.blit(wall_image, (col * cell_size, 250 + row * cell_size))
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
    coin_cells = set()  # Set to store coin cells
    lever_cell = None  # Variable to store lever cell
    wall_positions = set()  # Set for wall positions
    walls_to_remove = set()  # Set for walls to remove

    # Font for the label
    font = pygame.font.SysFont(None, 36)
    label_text = "Select reward states"

    # Button setup
    continue_button = Button(600, 10, 150, 40, "Continue")
    save_button = Button(10, 100, 80, 30, "Save")

    # Input box for reward
    reward_input_active = False
    reward_input_box = InputBox(10, 60, 140, 32, '')

    step = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if step == 0:
                label_text = "Select reward states and enter rewards"
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
                        if 0 <= col < int(information['grid_size']) and 250 <= y < 250 + int(information['grid_size']) * cell_size:
                            if (row, col) in selected_cells:
                                del selected_cells[(row, col)]
                            else:
                                reward_input_active = (row, col)

            elif step == 1:
                label_text = "Select slippery cells"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = x // cell_size
                    row = (y - 250) // cell_size
                    if 0 <= col < int(information['grid_size']) and 250 <= y < 250 + int(information['grid_size']) * cell_size:
                        if (row, col) in slippery_cells:
                            slippery_cells.remove((row, col))
                        else:
                            slippery_cells.add((row, col))

            elif step == 2:
                label_text = "Select coin locations"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = x // cell_size
                    row = (y - 250) // cell_size
                    if 0 <= col < int(information['grid_size']) and 250 <= y < 250 + int(information['grid_size']) * cell_size:
                        if (row, col) in coin_cells:
                            coin_cells.remove((row, col))
                        else:
                            coin_cells.add((row, col))

            elif step == 3:
                label_text = "Select lever location"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = x // cell_size
                    row = (y - 250) // cell_size
                    if 0 <= col < int(information['grid_size']) and 250 <= y < 250 + int(information['grid_size']) * cell_size:
                        if lever_cell == (row, col):
                            lever_cell = None
                        elif (row, col) not in selected_cells:
                            lever_cell = (row, col)

            elif step == 4:
                label_text = "Select wall positions"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = x // cell_size
                    row = (y - 250) // cell_size
                    if 0 <= col < int(information['grid_size']) and 250 <= y < 250 + int(information['grid_size']) * cell_size:
                        if (row, col) in wall_positions:
                            wall_positions.remove((row, col))
                        else:
                            wall_positions.add((row, col))

            elif step == 5:
                label_text = "Select walls to remove when lever is triggered"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = x // cell_size
                    row = (y - 250) // cell_size
                    if 0 <= col < int(information['grid_size']) and 250 <= y < 250 + int(information['grid_size']) * cell_size:
                        if (row, col) in walls_to_remove:
                            walls_to_remove.remove((row, col))
                        elif (row, col) in wall_positions:
                            walls_to_remove.add((row, col))

            result = continue_button.handle_event(event)
            if result == "Continue":
                step += 1
                if step > 5:
                    running = False
                    information['rewards'] = selected_cells
                    information['slippery'] = slippery_cells
                    information['coins'] = coin_cells
                    information['lever'] = lever_cell
                    information['walls'] = wall_positions
                    information['walls_to_remove'] = walls_to_remove

        screen.fill(const.BG_COLOR)
        cell_size = min(const.SCREEN_WIDTH // int(information['grid_size']),
                        (const.SCREEN_HEIGHT - 250) // int(information['grid_size']))
        draw_label(screen, label_text, font, const.TEXT_COLOR, 10, 10)

        continue_button.draw(screen)
        if reward_input_active and step == 0:
            draw_label(screen, "Press Enter to save reward:", font, const.TEXT_COLOR, 10, 30)
            reward_input_box.draw(screen)
            save_button.draw(screen)

        draw_grid(screen, int(information['grid_size']), int(information['grid_size']), cell_size, selected_cells,
                  slippery_cells, coin_cells, lever_cell, wall_positions, walls_to_remove)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    return information
