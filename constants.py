#e constants.py
import pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
GRAY_COLOR = (128, 128, 128)
BG_COLOR = (255, 255, 255)
GRID_COLOR = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)
INPUT_COLOR = (230, 230, 230)
FONT = pygame.font.Font(None, 22)
BUTTON_COLOR = (200, 200, 200)
HOVER_COLOR = (173, 216, 230)
CELL_EVEN_COLOR = (128, 128, 128)
CELL_ODD_COLOR = (152, 152, 152)
START_POSITION = (0, 0)
GLOW_COLOR = (255, 0, 0)  # Change this to the desired glow color
CELL_SIZE = 50
POSITIVE_REWARD_COLOR = (0, 255, 0)  # Green for positive reward
NEGATIVE_REWARD_COLOR = (255, 0, 0)  # Red for negative reward
SLIPPERY_COLOR = (0, 255, 255)  # Aqua color for slippery cells
ACTION_SPACE = ('U', 'D', 'L', 'R')