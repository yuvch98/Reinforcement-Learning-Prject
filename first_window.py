#e first_window.py

import constants as const
import pygame
import pygame.locals as pl

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
BG_COLOR = (255, 255, 255)
GRID_COLOR = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)
INPUT_COLOR = (230, 230, 230)
FONT = pygame.font.Font(None, 22)


# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Grid Input Interface")

# Text input class
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = INPUT_COLOR
        self.text = text
        self.txt_surface = FONT.render(text, True, TEXT_COLOR)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = (150, 150, 150) if self.active else INPUT_COLOR
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, TEXT_COLOR)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


def draw_grid(screen, grid_x, grid_y, cell_size):
    for row in range(grid_x):
        for col in range(grid_y):
            rect = pygame.Rect(col * cell_size, 250 + row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)


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

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for box in input_boxes:
                box.handle_event(event)

        screen.fill(BG_COLOR)

        # Draw labels and input boxes
        for i, box in enumerate(input_boxes):
            label_surface = FONT.render(labels[i], True, TEXT_COLOR)
            screen.blit(label_surface, (box.rect.x - 110, box.rect.y + 5))
            box.draw(screen)

        try:
            grid_x = int(input_boxes[0].text)
            grid_y = int(input_boxes[1].text)

            # Ensure values are between 1 and 10
            if 1 <= grid_x <= 10 and 1 <= grid_y <= 10:
                cell_size = min(SCREEN_WIDTH // grid_y, (SCREEN_HEIGHT - 250) // grid_x)
                draw_grid(screen, grid_x, grid_y, cell_size)
            else:
                error_surface = FONT.render("Values must be between 1 and 10", True, (255, 0, 0))
                screen.blit(error_surface, (SCREEN_WIDTH // 2 - error_surface.get_width() // 2, SCREEN_HEIGHT // 2))
        except ValueError:
            pass

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
