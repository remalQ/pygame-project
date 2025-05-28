import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image=None):
        """
        Базовый класс платформы, все платформы наследуются от него.
        """
        super().__init__()
        if image:
            # Если есть изображение — масштабируем под размер
            self.image = pygame.transform.scale(image, (width, height))
        else:
            # Если изображения нет — просто серый прямоугольник
            self.image = pygame.Surface((width, height))
            self.image.fill((150, 150, 150))  # Стандартный серый цвет

        self.rect = self.image.get_rect(topleft=(x, y))  # Позиция платформы

    def update(self, *args, **kwargs):
        """
        Базовый update — для потомков, сам по себе ничего не делает
        """
        pass
