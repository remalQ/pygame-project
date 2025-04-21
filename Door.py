from Const_Values import *

"""
Класс Door

Отвечает за создание и отображение дверей в игре. Дверь является спрайтом, который можно использовать для перехода между уровнями.
"""


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.opened_original = pygame.image.load('Assets/opened_door.png')
        self.closed_original = pygame.image.load('Assets/closed_door.png')

        # Размер двери: 2x4 тайла
        self.width = tile_size * 2
        self.height = tile_size * 4

        self.opened = pygame.transform.scale(self.opened_original, (self.width, self.height))
        self.closed = pygame.transform.scale(self.closed_original, (self.width, self.height))

        self.image = self.closed

        self.rect = self.image.get_rect(bottomleft=(x, y + tile_size * 2))

    def update(self, player=None, coins_group=None):
        if coins_group is not None and len(coins_group) == 0:
            self.image = self.opened
        else:
            self.image = self.closed

