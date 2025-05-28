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
from Platforms.PasswordBox import PasswordBox

class World:
    def __init__(self, data, door_group, coin_group, player):
        """Создаёт игровой мир и инициализирует все объекты уровня"""
        self.player = player
        self.tile_list = []
        self.platform_group = pygame.sprite.Group()
        self.breaking_platform_group = pygame.sprite.Group()
        self.hover_visible_platform_group = pygame.sprite.Group()
        self.moving_platform_group = pygame.sprite.Group()
        self.bouncing_platform_group = pygame.sprite.Group()
        self.drawable_platform_group = pygame.sprite.Group()
        self.door_group = door_group
        self.coin_group = coin_group
        self.clone_group = pygame.sprite.Group()
        self.password_group = pygame.sprite.Group()
        self.clone = None
        self.zones = []
        # Предзагружаем нужные текстуры
        self.textures = {
            1: pygame.image.load("Assets/platform.png").convert_alpha(),
            4: None,
            7: None
        }
        # Разбираем данные уровня (dict или list)
        if isinstance(data, dict):
            level_data = data.get('grid', [])
            self.texts = data.get('texts', [])
            self.zones = data.get('zones', [])
            self.password_positions = data.get('password_positions', [])
        else:
            level_data = data
            self.texts = []
            self.password_positions = []
        # Создаём игровые объекты по сетке уровня
        for row_idx, row in enumerate(level_data):
            for col_idx, tile in enumerate(row):
                x, y = col_idx * TILE_SIZE, row_idx * TILE_SIZE
                if tile == 1:
                    img = self.textures[1]
                    p = Platform(x, y, TILE_SIZE, TILE_SIZE, img)
                    self.platform_group.add(p)
                elif tile == 2:
                    # Генерируем дверь (2х2 клетки)
                    if (row_idx < len(level_data)-1 and col_idx < len(row)-1 and
                        level_data[row_idx][col_idx+1] == 2 and
                        level_data[row_idx+1][col_idx] == 2 and
                        level_data[row_idx+1][col_idx+1] == 2):
                        door = Door(x, y)
                        self.door_group.add(door)
                        # Убираем из сетки лишние клетки двери
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
        # Добавляем password box на нужные позиции
        for pos in self.password_positions:
            w = pos.get('w', TILE_SIZE * 4)
            h = pos.get('h', TILE_SIZE * 4)
            pb = PasswordBox(pos['x'], pos['y'], w, h)
            self.password_group.add(pb)
            self.platform_group.add(pb)

    def add_drawable_platform(self, x, y):
        """Добавляет временную платформу (нарисованную игроком)"""
        img = self.textures.get(1)
        p = Platform(x, y, TILE_SIZE, TILE_SIZE, img)
        self.drawable_platform_group.add(p)

    def reset_drawable_platforms(self):
        """Удаляет все временные платформы"""
        self.drawable_platform_group.empty()

    def check_password(self, level):
        """Проверяет пароль на уровне 8 (ожидается 404)"""
        if level != 8:
            return True  # Пароль не требуется на других уровнях
        if len(self.password_positions) != 3:  # Проверяем количество позиций
            return False
        correct_password = [4, 0, 4]
        current_password = [pb.get_digit() for pb in sorted(self.password_group, key=lambda pb: pb.rect.x)]
        return current_password == correct_password

    def draw(self, screen):
        """Рисует все объекты уровня на экране"""
        self.platform_group.draw(screen)
        self.breaking_platform_group.draw(screen)
        self.hover_visible_platform_group.draw(screen)
        self.moving_platform_group.draw(screen)
        self.bouncing_platform_group.draw(screen)
        self.drawable_platform_group.draw(screen)
        self.coin_group.update()
        self.coin_group.draw(screen)
        self.door_group.draw(screen)
        self.password_group.draw(screen)
        # Рисуем клонов (если есть)
        if self.clone:
            for clone in self.clone_group:
                screen.blit(clone.image, (clone.rect.x - clone.offset_x, clone.rect.y))
        # Рисуем игрока
        screen.blit(self.player.image, (self.player.rect.x - self.player.offset_x, self.player.rect.bottom - self.player.image.get_height()))
        # Рисуем текстовые подсказки уровня
        for t in self.texts:
            try:
                font = pygame.font.Font("Fonts/Monocraft.otf", t['font_size'])
                surf = font.render(t['text'], True, (0, 0, 0))
                screen.blit(surf, (t['x'], t['y']))
            except Exception as e:
                print(f"Ошибка отрисовки текста: {t}: {e}")
        # Рисуем зоны (например, зоны гравитации)
        for z in self.zones:
            s = pygame.Surface((z['w'], z['h']), pygame.SRCALPHA)
            s.fill((255, 165, 0, 0))
            screen.blit(s, (z['x'], z['y']))

    def update(self, level=None, stop_broken=None):
        """Обновляет состояние всех объектов уровня"""
        # Обновляем все платформы
        for grp in (
                self.breaking_platform_group,
                self.hover_visible_platform_group,
                self.moving_platform_group,
                self.bouncing_platform_group
        ):
            for p in grp.sprites():
                p.update()
        # Сохраняем флаг выхода в меню для уровня 4
        if stop_broken is not None:
            self.stop_broken = stop_broken
        # Обновляем двери с учётом уровня и мира
        for d in self.door_group:
            d.update(self.player, self.coin_group, level=level, world=self)
        # Сброс гравитации и ghost_mode каждый кадр
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

    def check_special_condition(self, level):
        """Проверяет специальные условия для прохождения уровня"""
        # Уровень 2: требуется определённая дистанция между игроком и клоном
        if level == 2:
            if not self.clone:
                return False
            dist = abs(self.player.rect.centerx - self.clone.rect.centerx)
            return dist >= 50
        # Уровень 4: разрешить завершение только если stop_broken=True (был вызвано меню)
        if level == 4:
            return getattr(self, "stop_broken", False)
        # Уровень 8: проверка пароля
        if level == 8:
            return self.check_password(level)
        # Для остальных уровней специальных условий нет
        return True
