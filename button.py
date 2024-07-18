import constants as const
import pygame


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = const.BUTTON_COLOR
        self.hover_color = const.HOVER_COLOR
        self.text = text
        pygame.init()
        self.txt_surface = const.FONT.render(text, True, const.TEXT_COLOR)

    def is_clicked(self, x, y):
        return self.rect.collidepoint((x, y))

    def handle_event(self, event) -> str:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.text
        return ""

    def draw(self, screen) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.txt_surface, (self.rect.x + (self.rect.w - self.txt_surface.get_width()) // 2,
                                       self.rect.y + (self.rect.h - self.txt_surface.get_height()) // 2))
        pygame.draw.rect(screen, const.TEXT_COLOR, self.rect, 2)
