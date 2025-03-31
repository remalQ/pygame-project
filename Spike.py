import pygame
from Create_Maps import TILE_SIZE


class Spike(pygame.sprite.Sprite):
    """Класс шипов (наносит урон игроку при контакте)."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Assets/spike.png")
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
