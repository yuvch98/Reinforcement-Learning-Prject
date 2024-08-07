import pygame
import sys
import matplotlib.pyplot as plt
from grid_world import standard_grid
from matplotlib.pyplot import style

style.use('fivethirtyeight')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
AQUA = (0, 255, 255)
CREAM = (255, 253, 208)

# Define the size of the grid and cells
CELL_SIZE = 100


def draw_grid(screen, grid):
    """
    Draws the grid on the screen.

    Args:
        screen (pygame.Surface): The Pygame surface to draw on.
        grid (Grid): The Grid object representing the environment.
    """
    for i in range(grid.rows):
        for j in range(grid.cols):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (i, j) in grid.walls:
                wall_image = pygame.image.load("wall.png").convert_alpha()
                wall_image = pygame.transform.scale(wall_image, (CELL_SIZE, CELL_SIZE))
                screen.blit(wall_image, (j * CELL_SIZE, i * CELL_SIZE))
                pygame.draw.rect(screen, BLACK, rect, 1)
            elif (i, j) in grid.slippery:
                slip_image = pygame.image.load("slippery.png").convert_alpha()
                slip_image = pygame.transform.scale(slip_image, (CELL_SIZE, CELL_SIZE))
                screen.blit(slip_image, (j * CELL_SIZE, i * CELL_SIZE))
                pygame.draw.rect(screen, BLACK, rect, 1)
            elif (i, j) in grid.coins:
                coin_image = pygame.image.load("coin.png").convert_alpha()
                coin_image = pygame.transform.scale(coin_image, (CELL_SIZE, CELL_SIZE))
                screen.blit(coin_image, (j * CELL_SIZE, i * CELL_SIZE))
                pygame.draw.rect(screen, BLACK, rect, 1)
            elif (i, j) == grid.lever and not grid.visited_lever:
                pygame.draw.rect(screen, WHITE, rect)
                lever_image = pygame.image.load("lever.png").convert_alpha()
                lever_image = pygame.transform.scale(lever_image, (CELL_SIZE, CELL_SIZE))
                screen.blit(lever_image, (j * CELL_SIZE, i * CELL_SIZE))
                pygame.draw.rect(screen, BLACK, rect, 1)
            else:
                pygame.draw.rect(screen, BLACK, rect, 1)


def draw_bot(screen, bot_image, position):
    """
    Draws the bot at the given position.

    Args:
        screen (pygame.Surface): The Pygame surface to draw on.
        bot_image (pygame.Surface): The image of the bot.
        position (tuple): The position (i, j) to draw the bot at.
    """
    x, y = position
    screen.blit(bot_image, (y * CELL_SIZE, x * CELL_SIZE))


def draw_rewards(screen, rewards, good_reward_image, bad_reward_image):
    """
    Draws the rewards at their respective positions.

    Args:
        screen (pygame.Surface): The Pygame surface to draw on.
        rewards (dict): Dictionary with positions as keys and rewards as values.
        good_reward_image (pygame.Surface): Image for good rewards.
        bad_reward_image (pygame.Surface): Image for bad rewards.
    """
    for (i, j), reward in rewards.items():
        if reward > 0:
            screen.blit(good_reward_image, (j * CELL_SIZE, i * CELL_SIZE))
        else:
            screen.blit(bad_reward_image, (j * CELL_SIZE, i * CELL_SIZE))


def draw_policeman(screen, policeman_image, position):
    """
    Draws the policeman at the given position.

    Args:
        screen (pygame.Surface): The Pygame surface to draw on.
        policeman_image (pygame.Surface): The image of the policeman.
        position (tuple): The position (i, j) to draw the policeman at.
    """
    x, y = position
    screen.blit(policeman_image, (y * CELL_SIZE, x * CELL_SIZE))


def main(game_info, play_phase=False, amount_of_plays=100):
    """
    Main function to run the game.

    Args:
        game_info (dict): Dictionary containing game configuration.
        play_phase (bool, optional): Flag to indicate if it's play phase. Default is False.
        amount_of_plays (int, optional): Number of plays to simulate. Default is 100.
    """
    grid_size = game_info['grid_size']
    policy = game_info['policy']
    rewards = game_info['rewards']
    slippery = game_info['slippery']
    q = game_info['q']
    walls = game_info['walls']
    coins = game_info['coins']
    lever = game_info['lever']
    reward_per_coin = game_info['reward_per_coins']
    walls_to_remove = game_info['walls_to_remove']

    grid = standard_grid(n=grid_size, rewards=rewards, slippery=slippery, q=q, walls=walls,
                         coins=coins, lever=lever, reward_per_coin=reward_per_coin,
                         walls_to_remove=walls_to_remove)

    pygame.init()
    screen = pygame.display.set_mode((grid_size * CELL_SIZE, grid_size * CELL_SIZE))
    pygame.display.set_caption("Policy Visualization")
    clock = pygame.time.Clock()

    bot_image = pygame.image.load("bot.png").convert_alpha()
    bot_image = pygame.transform.scale(bot_image, (CELL_SIZE, CELL_SIZE))
    good_reward_image = pygame.image.load("trophy.png").convert_alpha()
    good_reward_image = pygame.transform.scale(good_reward_image, (CELL_SIZE, CELL_SIZE))
    bad_reward_image = pygame.image.load("skull.png").convert_alpha()
    bad_reward_image = pygame.transform.scale(bad_reward_image, (CELL_SIZE, CELL_SIZE))
    policeman_image = pygame.image.load("policeman.png").convert_alpha()
    policeman_image = pygame.transform.scale(policeman_image, (CELL_SIZE, CELL_SIZE))

    fig, ax = plt.subplots()
    ax.scatter([], [])
    ax.set_ylim(min(grid.rewards.values()) + grid.policeman.reward,
                max(grid.rewards.values()) + ((len(grid.coins)) * grid.reward_coin))
    ax.set_xlim(0, amount_of_plays)
    ax.set_title("Rewards Over Plays")  # Add title to the plot
    plt.ion()
    plt.show()

    reward_data = []

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(CREAM)  # Clear the screen
        draw_rewards(screen, rewards, good_reward_image, bad_reward_image)
        draw_grid(screen, grid)  # Draw grid after rewards to ensure visibility

        if play_phase:
            reward_per_play = []
            # For the play phase, simulate plays
            for play_index in range(amount_of_plays):
                grid.reset()  # Start position
                grid.policeman.reset_police()
                s = grid.current_state()
                reward = 0
                while s in policy:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            break

                    if not running:
                        break

                    screen.fill(CREAM)  # Clear the screen
                    draw_rewards(screen, rewards, good_reward_image, bad_reward_image)
                    draw_grid(screen, grid)
                    draw_bot(screen, bot_image, s)
                    draw_policeman(screen, policeman_image, grid.policeman.get_pos())
                    pygame.display.flip()
                    pygame.time.delay(400)  # Adjust delay for speed of animation

                    # Move policeman and check for collision
                    if grid.policeman.get_pos() == s:
                        reward += grid.policeman.reward
                        reward_per_play.append(reward)
                        print("Game Over")
                        break

                    grid.policeman.move()
                    reward += grid.move(policy[s], grid.q)
                    s = grid.current_state()
                    draw_grid(screen, grid)
                    draw_bot(screen, bot_image, s)
                    draw_policeman(screen, policeman_image, grid.policeman.get_pos())
                    pygame.display.flip()
                    pygame.time.delay(20)
                print(reward)
                reward_per_play.append(reward)
                reward_data.append((play_index, reward))

                ax.cla()  # Clear previous scatter plot
                ax.scatter([x for x, y in reward_data], [y for x, y in reward_data], s=100)
                ax.set_ylim(min(grid.policeman.reward, min(grid.rewards.values()) - 10),
                            (max(grid.rewards.values()) + (len(grid.coins) * grid.reward_coin)) * 2 + 5)
                ax.set_xlim(0, play_index + 1)
                ax.set_title("Rewards Over Plays")  # Set title again after clearing axes
                plt.draw()
                plt.pause(0.1)  # Allow plot to update

                if not running:
                    break

            play_phase = False  # Ensure play phase runs only once

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    plt.close()
    sys.exit()


def get_next_state(state, action):
    """
    Returns the next state given the current state and action.

    Args:
        state (tuple): Current position (i, j).
        action (str): Action to be taken ('U', 'D', 'L', 'R').

    Returns:
        tuple: New position (i, j) after the action is taken.
    """
    i, j = state
    if action == 'U':
        return i - 1, j
    elif action == 'D':
        return i + 1, j
    elif action == 'L':
        return i, j - 1
    elif action == 'R':
        return i, j + 1
    return state
