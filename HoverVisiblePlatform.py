import pygame
from Platform import Platform


class HoverVisiblePlatform(Platform):
    def __init__(self, x, y, width, height, image=None):
        super().__init__(x, y, width, height, image)
        self.original_image = self.image.copy()
        self.image.set_alpha(0)  # Изначально невидима
        self.hovered = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if not self.hovered:
                self.image = self.original_image.copy()
                self.image.set_alpha(255)  # Платформа становится полностью видимой
                self.hovered = True
        else:
            if self.hovered:
                self.image.set_alpha(0)  # Платформа снова невидима
                self.hovered = False
