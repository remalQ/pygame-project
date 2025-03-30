import pygame
from Create_Maps import TILE_SIZE


class Coin(pygame.sprite.Sprite):
    """Класс монет (можно собирать для очков)."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("img/coin.png")
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
