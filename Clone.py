import pygame
from Const_Values import DEFAULT_GRAVITY, HEIGHT
from Create_Maps import TILE_SIZE

class Clone(pygame.sprite.Sprite):
    def __init__(self, player, world):
        super().__init__()
        self.player = player
        self.world = world  # Ссылка на мир для доступа к платформам и зонам
        self.image = player.image.copy()
        self.image.set_alpha(128)  # Полупрозрачность для отличия
        self.rect = player.rect.copy()
        self.rect.x -= 20  # Смещаем клона левее игрока на 20 пикселей
        # Параметры движения синхронизируются с игроком
        self.vel_x = 0
        self.vel_y = 0
        self.fall_speed = 0
        self.gravity = player.gravity
        self.in_air = True
        self.falling_mode = player.falling_mode
        self.direction = player.direction
        self.jumped = False
        self.base_jump_speed = player.base_jump_speed
        self.max_fall_speed = player.max_fall_speed
        self.can_pass_walls = False  # Учитываем ghost_mode
        self.index = 0
        self.counter = 0
        self.walk_cooldown = 3
        # Параметры для отскока
        self.vertical_bouncing = False
        self.vertical_bounce_speed = 0
        self.vertical_bounce_deceleration = 0
        self.horizontal_bouncing = False
        self.horizontal_bounce_speed = 0
        self.horizontal_bounce_deceleration = 0
        # Анимации
        self.images_right = [img.copy() for img in player.images_right]
        self.images_left = [img.copy() for img in player.images_left]
        self.jump_image_right = player.jump_image_right.copy()
        self.jump_image_left = player.jump_image_left.copy()
        for img in self.images_right + self.images_left + [self.jump_image_right, self.jump_image_left]:
            img.set_alpha(128)

    def start_vertical_bounce(self, initial_speed, deceleration):
        """Запускает вертикальный отскок."""
        self.vertical_bounce_speed = initial_speed
        self.vertical_bounce_deceleration = deceleration
        self.vertical_bouncing = True

    def start_horizontal_bounce(self, initial_speed, deceleration):
        """Запускает горизонтальный отскок."""
        self.horizontal_bounce_speed = initial_speed
        self.horizontal_bounce_deceleration = deceleration
        self.horizontal_bouncing = True

    def update(self, dx, dy, vel_x, vel_y, fall_speed, falling_mode, jumped, direction, gravity, in_air, keys):
        # Синхронизируем параметры с игроком
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.fall_speed = fall_speed
        self.falling_mode = falling_mode
        self.jumped = jumped
        self.direction = direction
        self.gravity = gravity
        self.in_air = in_air

        # Проверяем зоны для ghost_mode и low_gravity
        self.can_pass_walls = False
        cx, cy = self.rect.center
        for z in self.world.zones:
            rect = pygame.Rect(z['x'], z['y'], z['w'], z['h'])
            if rect.collidepoint(cx, cy):
                if z['effect'] == 'low_gravity':
                    self.gravity = DEFAULT_GRAVITY * z['value']
                elif z['effect'] == 'ghost_mode':
                    self.can_pass_walls = True

        # Все платформы для коллизий
        all_tiles = (
            self.world.platform_group.sprites() +
            self.world.breaking_platform_group.sprites() +
            self.world.hover_visible_platform_group.sprites() +
            self.world.moving_platform_group.sprites() +
            self.world.drawable_platform_group.sprites()
        )

        # Проверка ghost_mode для платформ
        def tile_in_ghost_zone(tile):
            for z in self.world.zones:
                if z['effect'] == 'ghost_mode':
                    zr = pygame.Rect(z['x'], z['y'], z['w'], z['h'])
                    if zr.colliderect(tile.rect):
                        return True
            return False

        # Учитываем отскок
        if self.vertical_bouncing:
            dy += self.vertical_bounce_speed
            if self.vertical_bounce_speed > 0:
                self.vertical_bounce_speed = max(0, self.vertical_bounce_speed - self.vertical_bounce_deceleration)
            else:
                self.vertical_bounce_speed = min(0, self.vertical_bounce_speed + self.vertical_bounce_deceleration)
            if self.vertical_bounce_speed == 0:
                self.vertical_bouncing = False

        if self.horizontal_bouncing:
            dx += self.horizontal_bounce_speed
            if self.horizontal_bounce_speed > 0:
                self.horizontal_bounce_speed = max(0, self.horizontal_bounce_speed - self.horizontal_bounce_deceleration)
            else:
                self.horizontal_bounce_speed = min(0, self.horizontal_bounce_speed + self.horizontal_bounce_deceleration)
            if self.horizontal_bounce_speed == 0:
                self.horizontal_bouncing = False

        # Горизонтальная коллизия
        rect_h = self.rect.copy()
        rect_h.x += dx
        for tile in all_tiles:
            if self.can_pass_walls and tile_in_ghost_zone(tile):
                continue
            if rect_h.colliderect(tile.rect):
                if dx > 0:
                    dx = tile.rect.left - self.rect.right
                elif dx < 0:
                    dx = tile.rect.right - self.rect.left
                self.vel_x = 0
                break

        # Вертикальная коллизия
        rect_v = self.rect.copy()
        rect_v.y += dy
        for tile in all_tiles:
            if self.can_pass_walls and tile_in_ghost_zone(tile):
                continue
            if rect_v.colliderect(tile.rect):
                if dy > 0:
                    dy = tile.rect.top - self.rect.bottom
                    self.vel_y = 0
                    self.fall_speed = 0
                    self.in_air = False
                elif dy < 0:
                    dy = tile.rect.bottom - self.rect.top
                    self.vel_y = 0
                    self.fall_speed = 0
                    self.in_air = True
                break

        # Коллизии с BouncingPlatform
        for tile in self.world.bouncing_platform_group.sprites():
            if self.can_pass_walls and tile_in_ghost_zone(tile):
                continue
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.rect.width, self.rect.height):
                bx, by = tile.apply_bounce(self)
                dx += bx
                dy += by

        # Применяем движение
        self.rect.x += dx
        self.rect.y += dy

        # Проверка земли
        foot = self.rect.move(0, 1)
        on_ground = False
        for tile in all_tiles:
            if self.can_pass_walls and tile_in_ghost_zone(tile):
                continue
            if foot.colliderect(tile.rect):
                on_ground = True
                break
        self.in_air = not on_ground
        if not self.in_air:
            self.falling_mode = False
            self.fall_speed = 0

        # Обновление анимации
        if self.in_air:
            self.image = self.jump_image_right if self.direction == 1 else self.jump_image_left
        else:
            if keys[pygame.K_a] or keys[pygame.K_d]:
                self.counter += 1
                if self.counter > self.walk_cooldown:
                    self.counter = 0
                    if self.direction == 1:
                        self.index = (self.index + 1) % len(self.images_right)
                    else:
                        self.index = (self.index + 1) % len(self.images_left)
                self.image = self.images_right[self.index] if self.direction == 1 else self.images_left[self.index]
            else:
                self.counter = 0
                self.index = 0
                self.image = self.images_right[0] if self.direction == 1 else self.images_left[0]
            self.image.set_alpha(128)