from Const_Values import *


# Класс кнопки
class Button:
    def __init__(self, text, x, y, color, hover_color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont(None, 40)
        self.rect = pygame.Rect(x - 100, y - 25, 200, 50)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surf = self.font.render(self.text, True, BLACK)
        screen.blit(text_surf, (self.x - text_surf.get_width() // 2, self.y - text_surf.get_height() // 2))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)