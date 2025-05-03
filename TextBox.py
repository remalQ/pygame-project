import pygame

class TextInputBox:
    def __init__(self, x, y, width, height, font_size=32, initial_text=""):

        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color('white')
        self.text = initial_text
        self.font = pygame.font.SysFont('Arial', font_size)
        self.active = False

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                if self.text:
                    return True
                return False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        return False

    def draw(self, screen):

        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))