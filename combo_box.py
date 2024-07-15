import pygame
import constants as const
class ComboBox:
    def __init__(self, x, y, w, h, font, options):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = const.BG_COLOR
        self.font = font
        self.options = options
        self.selected_option = options[0]
        self.show_options = False
        self.option_rects = [pygame.Rect(x, y + (i + 1) * h, w, h) for i in range(len(options))]

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text = self.font.render(self.selected_option, True, const.TEXT_COLOR)
        screen.blit(text, (self.rect.x + 10, self.rect.y + 10))

        if self.show_options:
            for i, rect in enumerate(self.option_rects):
                pygame.draw.rect(screen, const.GRAY_COLOR, rect)
                option_text = self.font.render(self.options[i], True, const.TEXT_COLOR)
                screen.blit(option_text, (rect.x + 10, rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.show_options = not self.show_options
            else:
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(event.pos):
                        self.selected_option = self.options[i]
                        self.show_options = False
                        break
                else:
                    self.show_options = False