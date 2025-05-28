import pygame
from Platforms.Platform import Platform
from Create_Maps import TILE_SIZE

class PasswordBox(Platform):
    def __init__(self, x, y, w=TILE_SIZE*4, h=TILE_SIZE*4):
        """
        Ячейка пароля, в которую можно кликать для смены цифры
        """
        super().__init__(x, y, w, h)
        self.digit = 0                                      # Текущая цифра ячейки
        font_size = int(min(w, h) * 0.5)
        self.font = pygame.font.Font("./fonts/Monocraft.otf", font_size)
        self.update_image()                                 # Рисуем ячейку

    def update_image(self):
        """
        Обновляет изображение ячейки после смены цифры
        """
        self.image.fill((255, 255, 255))  # Белый фон
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, self.rect.width, self.rect.height), 3)  # Чёрная рамка
        text_surface = self.font.render(str(self.digit), True, (0, 0, 0))
        text_outline = self.font.render(str(self.digit), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        # Обводка для читаемости
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                outline_rect = text_surface.get_rect(center=(self.rect.width // 2 + dx, self.rect.height // 2 + dy))
                self.image.blit(text_outline, outline_rect)
        self.image.blit(text_surface, text_rect)

    def handle_click(self):
        """
        Обрабатывает клик мыши — меняет цифру
        """
        self.digit = (self.digit + 1) % 10
        self.update_image()

    def get_digit(self):
        """Возвращает текущую цифру ячейки"""
        return self.digit
