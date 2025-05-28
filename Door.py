from Const_Values import *
import pygame

class Door(pygame.sprite.Sprite):
    """Класс двери — для входа и выхода с уровня"""

    def __init__(self, x, y):
        """Создаёт дверь на уровне"""
        super().__init__()
        self.opened_original = pygame.image.load('Assets/opened_door.png')
        self.closed_original = pygame.image.load('Assets/closed_door.png')
        self.width = tile_size * 2
        self.height = tile_size * 4
        self.opened = pygame.transform.scale(self.opened_original, (self.width, self.height))
        self.closed = pygame.transform.scale(self.closed_original, (self.width, self.height))
        self.image = self.closed
        self.rect = self.image.get_rect(bottomleft=(x, y + tile_size * 2))

    def update(self, player=None, coins_group=None, level=None, world=None):
        """Обновляет состояние (открыта/закрыта) двери"""
        all_coins_collected = (coins_group is None or len(coins_group) == 0)
        special_condition = True
        if world is not None and hasattr(world, 'check_special_condition'):
            special_condition = world.check_special_condition(level)
        if all_coins_collected and special_condition:
            self.image = self.opened
        else:
            self.image = self.closed
