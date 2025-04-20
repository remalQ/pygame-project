import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image=None):
        super().__init__()
        if image:
            self.image = pygame.transform.scale(image, (width, height))
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill((150, 150, 150))  # Стандартный серый цвет, если текстура не передана

        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, *args, **kwargs):
        pass
