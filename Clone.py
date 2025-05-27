import pygame
from Const_Values import DEFAULT_GRAVITY
from Create_Maps import TILE_SIZE

class Clone(pygame.sprite.Sprite):
    def __init__(self, player, world):
        super().__init__()
        self.player = player
        self.world = world

        self.hitbox_width = player.hitbox_width  # 28
        self.hitbox_height = player.hitbox_height  # 90
        self.offset_x = player.offset_x  # 26

        self.images_right = [img.copy() for img in player.images_right]
        self.images_left = [img.copy() for img in player.images_left]
        self.jump_image_right = player.jump_image_right.copy()
        self.jump_image_left = player.jump_image_left.copy()
        for img in self.images_right + self.images_left + [self.jump_image_right, self.jump_image_left]:
            img.set_alpha(128)

        self.direction = 1
        self.image = self.images_right[0]
        self.index = 0
        self.counter = 0

        # СПРАЙТ клона рисуется как у игрока: (rect.x - offset_x, rect.y)
        # Поэтому rect должен быть без offset_x
        spawn_gap = 8  # Измени на нужное число для контроля расстояния (0 — вплотную, 2-4 — чуть левее)
        clone_hitbox_x = player.rect.x - self.hitbox_width - spawn_gap
        clone_hitbox_y = player.rect.y

        self.rect = pygame.Rect(
            clone_hitbox_x,
            clone_hitbox_y,
            self.hitbox_width,
            self.hitbox_height
        )

        # Остальное как у тебя...
        self.vel_x = 0
        self.vel_y = 0
        self.base_jump_speed = player.base_jump_speed
        self.max_fall_speed = player.max_fall_speed
        self.jumped = False
        self.in_air = True
        self.gravity = player.gravity if hasattr(player, 'gravity') else 1
        self.falling_mode = False
        self.fall_speed = 0
        self.vertical_bouncing = False
        self.vertical_bounce_speed = 0
        self.vertical_bounce_deceleration = 0
        self.horizontal_bouncing = False
        self.horizontal_bounce_speed = 0
        self.horizontal_bounce_deceleration = 0
        self.can_pass_walls = False

    def start_vertical_bounce(self, initial_speed, deceleration):
        self.vertical_bounce_speed = initial_speed
        self.vertical_bounce_deceleration = deceleration
        self.vertical_bouncing = True

    def start_horizontal_bounce(self, initial_speed, deceleration):
        self.horizontal_bounce_speed = initial_speed
        self.horizontal_bounce_deceleration = deceleration
        self.horizontal_bouncing = True

    def update(self, keys, direction, jumped):
        dx, dy = 0, 0
        walk_cooldown = 3

        # Проверка зон (low_gravity, ghost_mode)
        self.gravity = DEFAULT_GRAVITY
        self.can_pass_walls = False
        cx, cy = self.rect.center
        for z in self.world.zones:
            rect = pygame.Rect(z['x'], z['y'], z['w'], z['h'])
            if rect.collidepoint(cx, cy):
                if z['effect'] == 'low_gravity':
                    self.gravity = DEFAULT_GRAVITY * z['value']
                elif z['effect'] == 'ghost_mode':
                    self.can_pass_walls = True

        # Равнозамедленный отскок
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

        # Горизонтальное скольжение
        if abs(self.vel_x) > 0:
            dx += self.vel_x
            self.vel_x *= 0.9

        # Управление (двойник всегда повторяет направление)
        if not self.falling_mode:
            if keys[pygame.K_a]:
                dx -= 5
                self.direction = -1
            if keys[pygame.K_d]:
                dx += 5
                self.direction = 1
            if keys[pygame.K_SPACE] and not self.jumped and not self.in_air:
                self.vel_y = -self.base_jump_speed
                self.jumped = True
            if not keys[pygame.K_SPACE]:
                self.jumped = False

        # Гравитация
        if self.falling_mode:
            self.fall_speed = min(self.fall_speed + 0.5, self.max_fall_speed)
            dy += self.fall_speed
        else:
            self.vel_y = min(self.vel_y + self.gravity, self.max_fall_speed)
            dy += self.vel_y

        # Проверка ghost_mode для платформ
        def tile_in_ghost_zone(tile):
            for z in self.world.zones:
                if z['effect'] == 'ghost_mode':
                    zr = pygame.Rect(z['x'], z['y'], z['w'], z['h'])
                    if zr.colliderect(tile.rect):
                        return True
            return False

        all_tiles = (
            self.world.platform_group.sprites() +
            self.world.breaking_platform_group.sprites() +
            self.world.hover_visible_platform_group.sprites() +
            self.world.moving_platform_group.sprites() +
            self.world.drawable_platform_group.sprites()
        )
        all_tiles += [d for d in self.world.door_group if d.image == d.closed]

        # --- 1. Горизонтальная коллизия (как у игрока) ---
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

        # --- 2. Вертикальная коллизия ---
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
                break

        # --- 3. Коллизии с BouncingPlatform (именно ПОСЛЕ платформ) ---
        for tile in self.world.bouncing_platform_group.sprites():
            if self.can_pass_walls and tile_in_ghost_zone(tile):
                continue
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.rect.width, self.rect.height):
                bx, by = tile.apply_bounce(self)
                dx += bx
                dy += by

        # --- 4. Применить движение ---
        self.rect.x += dx
        self.rect.y += dy

        # --- 5. Проверка земли ---
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

        # --- 6. Анимация ---
        if self.in_air:
            self.image = self.jump_image_right if self.direction == 1 else self.jump_image_left
        else:
            if keys[pygame.K_a] or keys[pygame.K_d]:
                self.counter += 1
                if self.counter > walk_cooldown:
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
