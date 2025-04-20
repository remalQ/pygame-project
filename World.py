from Create_Maps import TILE_SIZE
from Const_Values import *
from Platforms.BreakingPlatform import BreakingPlatform
from Door import Door
from Coin import Coin
from Platforms.Platform import Platform
from Platforms.HoverVisiblePlatform import HoverVisiblePlatform
from Platforms.MovingPlatform import MovingPlatform


class World:
    """Класс World создает игровой мир на основе загруженных данных и отрисовывает его."""

    def __init__(self, data, door_group, coin_group, player):
        self.tile_list = []
        self.platform_group = pygame.sprite.Group()
        self.door_group = door_group
        self.coin_group = coin_group
        self.breaking_platform_group = pygame.sprite.Group()
        self.hover_visible_platform_group = pygame.sprite.Group()
        self.moving_platform_group = pygame.sprite.Group()

        self.textures = {
            1: pygame.image.load("Assets/platform.png").convert_alpha(),
            4: None
        }

        for row_count, row in enumerate(data):
            for col_count, tile in enumerate(row):
                x, y = col_count * TILE_SIZE, row_count * TILE_SIZE

                if tile == 1:
                    img = self.textures[1]
                    platform = Platform(x, y, TILE_SIZE, TILE_SIZE, img)
                    self.platform_group.add(platform)

                elif tile == 2:
                    if (row_count < len(data) - 1 and col_count < len(row) - 1 and
                            data[row_count][col_count + 1] == 2 and
                            data[row_count + 1][col_count] == 2 and
                            data[row_count + 1][col_count + 1] == 2):
                        door = Door(x, y)
                        self.door_group.add(door)
                        data[row_count][col_count + 1] = 0
                        data[row_count + 1][col_count] = 0
                        data[row_count + 1][col_count + 1] = 0

                elif tile == 3:
                    coin = Coin(x, y)
                    self.coin_group.add(coin)

                elif tile == 4:
                    platform = BreakingPlatform(x, y, TILE_SIZE, TILE_SIZE)
                    self.breaking_platform_group.add(platform)

                elif tile == 5:
                    platform = HoverVisiblePlatform(x, y, TILE_SIZE, TILE_SIZE)
                    self.hover_visible_platform_group.add(platform)

                elif tile == 6:
                    platform = MovingPlatform(x, y, TILE_SIZE, TILE_SIZE, player)
                    self.moving_platform_group.add(platform)

    def draw(self, screen):
        self.platform_group.draw(screen)
        self.door_group.draw(screen)
        self.coin_group.update()
        self.coin_group.draw(screen)
        self.breaking_platform_group.draw(screen)
        self.hover_visible_platform_group.draw(screen)
        self.moving_platform_group.draw(screen)

    def update(self):
        """Обновляет поведение интерактивных объектов"""
        for platform in self.breaking_platform_group.sprites() + self.hover_visible_platform_group.sprites() \
                + self.moving_platform_group.sprites():
            platform.update()

