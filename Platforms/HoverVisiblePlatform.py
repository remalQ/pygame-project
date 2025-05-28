import pygame
from Platforms.Platform import Platform

class HoverVisiblePlatform(Platform):
    def __init__(self, x, y, width, height, image=None):
        """
        Создаёт невидимую платформу, которая становится видимой при наведении курсора
        """
        super().__init__(x, y, width, height, image)
        self.original_image = self.image.copy()  # Сохраняем исходную текстуру
        self.image.set_alpha(0)                  # Платформа по умолчанию невидима
        self.hovered = False                     # Флаг: наведён ли курсор

    def update(self):
        """
        Проверяет, находится ли курсор мыши над платформой и меняет её видимость
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if not self.hovered:
                self.image = self.original_image.copy()
                self.image.set_alpha(255)  # Делаем платформу видимой
                self.hovered = True
        else:
            if self.hovered:
                self.image.set_alpha(0)    # Снова делаем невидимой
                self.hovered = False
