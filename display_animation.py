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

# Define the size of the grid and cells
CELL_SIZE = 128

def draw_grid(screen, grid_size, slippery):
    for i in range(grid_size):
        for j in range(grid_size):
            if (i, j) not in slippery:
                rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, WHITE, rect, 1)
            else:
                rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, AQUA, rect)

def draw_bot(screen, bot_image, position):
    x, y = position
    screen.blit(bot_image, (y * CELL_SIZE, x * CELL_SIZE))

def draw_rewards(screen, rewards, good_reward_image, bad_reward_image):
    for (i, j), reward in rewards.items():
        if reward > 0:
            screen.blit(good_reward_image, (j * CELL_SIZE, i * CELL_SIZE))
        else:
            screen.blit(bad_reward_image, (j * CELL_SIZE, i * CELL_SIZE))

def draw_policeman(screen, policeman_image, position):
    x, y = position
    screen.blit(policeman_image, (y * CELL_SIZE, x * CELL_SIZE))

def main(game_info, play_phase=False, amount_of_plays=100, reward_queue=None):
    grid_size = game_info['grid_size']
    policy = game_info['policy']
    rewards = game_info['rewards']
    slippery = game_info['slippery']
    q = game_info['q']
    grid = standard_grid(grid_size, rewards, slippery, q)

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
    scatter = ax.scatter([], [])
    ax.set_ylim(-10, 10)
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

        screen.fill(BLACK)  # Clear the screen
        draw_rewards(screen, rewards, good_reward_image, bad_reward_image)
        draw_grid(screen, grid_size, slippery)  # Draw grid after rewards to ensure visibility

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

                    screen.fill(BLACK)  # Clear the screen
                    draw_rewards(screen, rewards, good_reward_image, bad_reward_image)
                    draw_grid(screen, grid_size, slippery)
                    draw_bot(screen, bot_image, s)
                    draw_policeman(screen, policeman_image, grid.policeman.get_pos())
                    pygame.display.flip()
                    pygame.time.delay(300)  # Adjust delay for speed of animation

                    # Move policeman and check for collision
                    if grid.policeman.get_pos() == s:
                        reward -= 10
                        reward_per_play.append(reward)
                        print("Game Over")
                        break

                    grid.policeman.move()
                    reward += grid.move(policy[s], grid.q)
                    s = grid.current_state()
                reward_per_play.append(reward)
                reward_data.append((play_index, reward))

                ax.cla()  # Clear previous scatter plot
                ax.scatter([x for x, y in reward_data], [y for x, y in reward_data], s=100)
                ax.set_ylim(-10, 10)
                ax.set_xlim(0, play_index + 1)
                ax.set_title("Rewards Over Plays")  # Set title again after clearing axes
                plt.draw()
                plt.pause(0.1)  # Allow plot to update

                if not running:
                    break

            play_phase = False  # Ensure play phase runs only once

        pygame.display.flip()
        clock.tick(30)
        running = False
    pygame.quit()
    plt.close()
    sys.exit()

def get_next_state(state, action):
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
