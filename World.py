import pygame
from Create_Maps import TILE_SIZE
from Const_Values import DEFAULT_GRAVITY
from Platforms.Platform import Platform
from Platforms.BreakingPlatform import BreakingPlatform
from Platforms.HoverVisiblePlatform import HoverVisiblePlatform
from Platforms.MovingPlatform import MovingPlatform
from Platforms.BouncingPlatform import BouncingPlatform
from Door import Door
from Coin import Coin
from Clone import Clone
#для коммита
class World:
    """Создает игровой мир из данных и применяет зоны с эффектами."""
    def __init__(self, data, door_group, coin_group, player):
        self.player = player
        self.tile_list = []
        # Группы спрайтов
        self.platform_group = pygame.sprite.Group()
        self.breaking_platform_group = pygame.sprite.Group()
        self.hover_visible_platform_group = pygame.sprite.Group()
        self.moving_platform_group = pygame.sprite.Group()
        self.bouncing_platform_group = pygame.sprite.Group()
        self.drawable_platform_group = pygame.sprite.Group()
        self.door_group = door_group
        self.coin_group = coin_group
        self.clone_group = pygame.sprite.Group()
        self.clone = None
        # Зоны с эффектами
        self.zones = []
        # Текстуры
        self.textures = {
            1: pygame.image.load("Assets/platform.png").convert_alpha(),
            4: None,
            7: None
        }
        # Разбираем данные уровня
        if isinstance(data, dict):
            level_data = data.get('grid', [])
            self.texts = data.get('texts', [])
            self.zones = data.get('zones', [])
        else:
            level_data = data
            self.texts = []
        # Создаём тайлы
        for row_idx, row in enumerate(level_data):
            for col_idx, tile in enumerate(row):
                x, y = col_idx * TILE_SIZE, row_idx * TILE_SIZE
                if tile == 1:
                    img = self.textures[1]
                    p = Platform(x, y, TILE_SIZE, TILE_SIZE, img)
                    self.platform_group.add(p)
                elif tile == 2:
                    # Дверь 2×2
                    if (row_idx < len(level_data)-1 and col_idx < len(row)-1 and
                        level_data[row_idx][col_idx+1] == 2 and
                        level_data[row_idx+1][col_idx] == 2 and
                        level_data[row_idx+1][col_idx+1] == 2):
                        door = Door(x, y)
                        self.door_group.add(door)
                        level_data[row_idx][col_idx+1] = 0
                        level_data[row_idx+1][col_idx] = 0
                        level_data[row_idx+1][col_idx+1] = 0
                elif tile == 3:
                    c = Coin(x, y)
                    self.coin_group.add(c)
                elif tile == 4:
                    bp = BreakingPlatform(x, y, TILE_SIZE, TILE_SIZE)
                    self.breaking_platform_group.add(bp)
                elif tile == 5:
                    hv = HoverVisiblePlatform(x, y, TILE_SIZE, TILE_SIZE)
                    self.hover_visible_platform_group.add(hv)
                elif tile == 6:
                    mp = MovingPlatform(x, y, TILE_SIZE, TILE_SIZE, self.player)
                    self.moving_platform_group.add(mp)
                elif tile == 7:
                    b = BouncingPlatform(x, y, TILE_SIZE, TILE_SIZE, None)
                    self.bouncing_platform_group.add(b)

    def add_drawable_platform(self, x, y):
        """Добавляет нарисованную платформу."""
        img = self.textures.get(1)
        p = Platform(x, y, TILE_SIZE, TILE_SIZE, img)
        self.drawable_platform_group.add(p)

    def reset_drawable_platforms(self):
        """Очищает нарисованные платформы."""
        self.drawable_platform_group.empty()

    def draw(self, screen):
        """Отрисовывает мир."""
        # Отрисовываем платформы
        self.platform_group.draw(screen)
        self.breaking_platform_group.draw(screen)
        self.hover_visible_platform_group.draw(screen)
        self.moving_platform_group.draw(screen)
        self.bouncing_platform_group.draw(screen)
        self.drawable_platform_group.draw(screen)
        self.coin_group.update()
        self.coin_group.draw(screen)
        self.door_group.draw(screen)
        # Отрисовываем клона, только если он существует
        if self.clone:
            self.clone_group.draw(screen)
        # Отрисовываем игрока последним, чтобы он был поверх клона
        screen.blit(self.player.image, (self.player.rect.x - self.player.offset_x, self.player.rect.bottom - self.player.image.get_height()))
        # Отрисовка текстов
        for t in self.texts:
            try:
                font = pygame.font.Font("Fonts/Monocraft.otf", t['font_size'])
                surf = font.render(t['text'], True, (0, 0, 0))
                screen.blit(surf, (t['x'], t['y']))
            except Exception as e:
                print(f"Ошибка отрисовки текста: {t}: {e}")
        # Отрисовка зон
        for z in self.zones:
            s = pygame.Surface((z['w'], z['h']), pygame.SRCALPHA)
            s.fill((255, 165, 0, 0))
            screen.blit(s, (z['x'], z['y']))

    def update(self):
        """Обновляет платформы и двери."""
        for grp in (self.breaking_platform_group,
                    self.hover_visible_platform_group,
                    self.moving_platform_group,
                    self.bouncing_platform_group):
            for p in grp.sprites():
                p.update()
        for d in self.door_group:
            d.update(self.player, self.coin_group)
        # Сбрасываем параметры игрока
        self.player.gravity = DEFAULT_GRAVITY
        self.player.can_pass_walls = False
        px, py = self.player.rect.center
        for z in self.zones:
            rect = pygame.Rect(z['x'], z['y'], z['w'], z['h'])
            if rect.collidepoint(px, py):
                if z['effect'] == 'low_gravity':
                    self.player.gravity = DEFAULT_GRAVITY * z['value']
                elif z['effect'] == 'ghost_mode':
                    self.player.can_pass_walls = True