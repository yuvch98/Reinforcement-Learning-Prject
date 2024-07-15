#e constants.py
import pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
BG_COLOR = (255, 255, 255)
GRID_COLOR = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)
INPUT_COLOR = (230, 230, 230)
FONT = pygame.font.Font(None, 22)
BUTTON_COLOR = (200, 200, 200)
HOVER_COLOR = (173, 216, 230)
CELL_EVEN_COLOR = (179, 225, 172)
CELL_ODD_COLOR = (115, 195, 108)
START_POSITION = (0, 0)
POLICEMAN_START_POSITION = (5, 5)
POLICEMAN_DIRECTION = "random"  # Options: "up", "down", "random"

ALGORITHM = "Q-Learning"  # Options: "Q-Learning", "SARSA"
TRAINING_GAMES = 1000
PLAYING_GAMES = 10

EPSILON = 0.1
ALPHA = 0.1
GAMMA = 0.9

CELL_SIZE = 50
WINDOW_TITLE = "Reinforcement Learning Game"