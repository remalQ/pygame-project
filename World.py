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
        self.drawable_platform_group = pygame.sprite.Group()  # Группа для рисованных платформ
        self.texts = []
        self.player = player
        self.allow_drawing = False  # По умолчанию рисование запрещено

        self.textures = {
            1: pygame.image.load("Assets/platform.png").convert_alpha(),
            4: None
        }

        if isinstance(data, dict):
            level_data = data.get('grid', [])
            self.texts = data.get('texts', [])
        else:
            level_data = data
            self.texts = []

        # Загрузка тайлов
        for row_count, row in enumerate(level_data):
            for col_count, tile in enumerate(row):
                x, y = col_count * TILE_SIZE, row_count * TILE_SIZE

                if tile == 1:
                    img = self.textures[1]
                    platform = Platform(x, y, TILE_SIZE, TILE_SIZE, img)
                    self.platform_group.add(platform)

                elif tile == 2:
                    if (row_count < len(level_data) - 1 and col_count < len(row) - 1 and
                            level_data[row_count][col_count + 1] == 2 and
                            level_data[row_count + 1][col_count] == 2 and
                            level_data[row_count + 1][col_count + 1] == 2):
                        door = Door(x, y)
                        self.door_group.add(door)
                        level_data[row_count][col_count + 1] = 0
                        level_data[row_count + 1][col_count] = 0
                        level_data[row_count + 1][col_count + 1] = 0

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
                    platform = MovingPlatform(x, y, TILE_SIZE, TILE_SIZE, self.player)
                    self.moving_platform_group.add(platform)

    def add_drawable_platform(self, x, y):
        """Добавляет рисованную платформу в указанных координатах"""
        img = self.textures[1] if 1 in self.textures else None
        platform = Platform(x, y, TILE_SIZE, TILE_SIZE, img)
        self.drawable_platform_group.add(platform)

    def reset_drawable_platforms(self):
        """Очищает все рисованные платформы"""
        self.drawable_platform_group.empty()

    def draw(self, screen):
        self.platform_group.draw(screen)
        self.door_group.draw(screen)
        self.coin_group.update()
        self.coin_group.draw(screen)
        self.breaking_platform_group.draw(screen)
        self.hover_visible_platform_group.draw(screen)
        self.moving_platform_group.draw(screen)
        self.drawable_platform_group.draw(screen)  # Отрисовка рисованных платформ

        for text_data in self.texts:
            font = pygame.font.Font("Fonts/Monocraft.otf", text_data['font_size'])
            text_surface = font.render(text_data['text'], True, (0, 0, 0))
            screen.blit(text_surface, (text_data['x'], text_data['y']))

    def update(self):
        """Обновляет поведение интерактивных объектов"""
        for platform in (self.breaking_platform_group.sprites() +
                         self.hover_visible_platform_group.sprites() +
                         self.moving_platform_group.sprites()):
            platform.update()

        for door in self.door_group:
            door.update(self.player, self.coin_group)