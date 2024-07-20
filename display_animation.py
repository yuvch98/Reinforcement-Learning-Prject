import pygame
import numpy as np
# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Define the size of the grid and cells
CELL_SIZE = 128


def draw_grid(screen, grid_size):
    for i in range(grid_size):
        for j in range(grid_size):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)


def draw_bot(screen, bot_image, position):
    x, y = position
    screen.blit(bot_image, (y * CELL_SIZE, x * CELL_SIZE))


def draw_rewards(screen, rewards, good_reward_image, bad_reward_image):
    for (i, j), reward in rewards.items():
        if reward > 0:
            screen.blit(good_reward_image, (j * CELL_SIZE, i * CELL_SIZE))
        else:
            screen.blit(bad_reward_image, (j * CELL_SIZE, i * CELL_SIZE))


def main(game_info, play_phase=False):
    grid_size = game_info['grid_size']
    policy = game_info['policy']
    rewards = game_info['rewards']
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

    screen.fill(WHITE)  # Clear the screen
    draw_rewards(screen, rewards, good_reward_image, bad_reward_image)
    draw_grid(screen, grid_size)  # Draw grid after rewards to ensure visibility
    pygame.display.flip()
    # Set up a timer event to trigger every second
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    policy_items = list(policy.items())
    current_index = 0
    running = True

    if play_phase:
        # For the play phase, simulate 100 plays
        plays = 100
        for _ in range(plays):
            s = (0, 0)  # Start position
            while s in policy:
                action = policy[s]
                screen.fill(BLACK)  # Clear the screen
                draw_rewards(screen, rewards, good_reward_image, bad_reward_image)
                draw_bot(screen, bot_image, s)
                draw_grid(screen, grid_size)  # Draw grid after bot to ensure visibility
                pygame.display.flip()
                pygame.time.delay(300)  # Adjust delay for speed of animation
                s = get_next_state(s, action)
            clock.tick(30)
    else:
        # Training phase visualization
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.USEREVENT:
                    if current_index < len(policy_items):
                        (i, j), action = policy_items[current_index]
                        screen.fill(WHITE)  # Clear the screen
                        draw_rewards(screen, rewards, good_reward_image, bad_reward_image)
                        draw_bot(screen, bot_image, (i, j))
                        draw_grid(screen, grid_size)  # Draw grid after bot to ensure visibility
                        pygame.display.flip()
                        current_index += 1
            clock.tick(30)
    pygame.quit()


def get_next_state(state, action):
    i, j = state
    if action == 'U':
        return (i - 1, j)
    elif action == 'D':
        return (i + 1, j)
    elif action == 'L':
        return (i, j - 1)
    elif action == 'R':
        return (i, j + 1)
    return state
