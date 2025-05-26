import pygame
from Const_Values import DEFAULT_GRAVITY, HEIGHT
from Create_Maps import TILE_SIZE


class Player:
    def __init__(self, x, y, coin_sound, jump_sound):
        self.hitbox_width = 28
        self.hitbox_height = 90
        self.offset_x = (80 - self.hitbox_width) // 2
        self.coin_sound = coin_sound
        self.jump_sound = jump_sound
        self.coins_collected = 0
        self.drawing_platform = False
        self.platform_start_pos = None
        self.platform_end_pos = None
        self.falling_mode = False
        self.fall_speed = 0
        self.vertical_bouncing = False
        self.vertical_bounce_speed = 0
        self.vertical_bounce_deceleration = 0
        self.horizontal_bouncing = False
        self.horizontal_bounce_speed = 0
        self.horizontal_bounce_deceleration = 0
        self.gravity = DEFAULT_GRAVITY
        self.can_pass_walls = False
        self.base_jump_speed = 15
        self.max_fall_speed = 15
        self.vel_x = 0
        self.jumped = False
        self.first_frame = True
        self.reset(x, y)

    def reset(self, x, y):
        # Загрузка анимаций
        self.images_right = []
        self.images_left = []
        for num in range(1, 5):
            img = pygame.image.load(f'Assets/frame{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (80, 90))
            self.images_right.append(img)
            self.images_left.append(pygame.transform.flip(img, True, False))
        self.jump_image_right = pygame.image.load('Assets/frame_jump.png').convert_alpha()
        self.jump_image_right = pygame.transform.scale(self.jump_image_right, (80, 90))
        self.jump_image_left = pygame.transform.flip(self.jump_image_right, True, False)
        self.direction = 1
        self.image = self.images_right[0]
        self.index = 0
        self.counter = 0
        self.rect = pygame.Rect(x, y, self.hitbox_width, self.hitbox_height)
        self.vel_y = 0
        self.in_air = True
        self.drawing_platform = False
        self.platform_start_pos = None
        self.platform_end_pos = None
        self.falling_mode = False
        self.fall_speed = 0
        self.first_frame = True
        self.gravity = DEFAULT_GRAVITY
        self.can_pass_walls = False
        self.vertical_bouncing = False
        self.vertical_bounce_speed = 0
        self.vertical_bounce_deceleration = 0
        self.horizontal_bouncing = False
        self.horizontal_bounce_speed = 0
        self.horizontal_bounce_deceleration = 0

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

    def start_falling(self):
        """Запускает режим падения."""
        self.falling_mode = True
        self.fall_speed = 3

    def update(self, game_over, world, door_group, coin_group, screen):
        dx, dy = 0, 0
        walk_cooldown = 3
        keys = pygame.key.get_pressed()

        # Проверка ghost_mode для платформ
        def tile_in_ghost_zone(tile):
            for z in world.zones:
                if z['effect'] == 'ghost_mode':
                    zr = pygame.Rect(z['x'], z['y'], z['w'], z['h'])
                    if zr.colliderect(tile.rect):
                        return True
            return False

        if game_over == 0:
            # 1) Рисование платформ (уровень 3)
            if getattr(world, 'allow_drawing', False):
                mx, my = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    if not self.drawing_platform:
                        self.drawing_platform = True
                        self.platform_start_pos = (mx // TILE_SIZE) * TILE_SIZE
                    self.platform_end_pos = (mx // TILE_SIZE) * TILE_SIZE
                else:
                    if self.drawing_platform:
                        self.drawing_platform = False
                        if self.platform_start_pos is not None and self.platform_end_pos is not None:
                            start_x = min(self.platform_start_pos, self.platform_end_pos)
                            end_x = max(self.platform_start_pos, self.platform_end_pos)
                            y_tile = (my // TILE_SIZE) * TILE_SIZE
                            for x in range(start_x, end_x+TILE_SIZE, TILE_SIZE):
                                world.add_drawable_platform(x, y_tile)
                        self.platform_start_pos = None
                        self.platform_end_pos = None

            # 2) Равнозамедленный отскок
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

            # 3) Горизонтальное скольжение
            if abs(self.vel_x) > 0:
                dx += self.vel_x
                self.vel_x *= 0.9

            # 4) Управление и прыжок
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
                    self.jump_sound.play()
                if not keys[pygame.K_SPACE]:
                    self.jumped = False

            # 5) Гравитация
            if self.falling_mode:
                self.fall_speed = min(self.fall_speed + 0.5, self.max_fall_speed)
                dy += self.fall_speed
            else:
                self.vel_y = min(self.vel_y + self.gravity, self.max_fall_speed)
                dy += self.vel_y

            # 6) Коллизии
            all_tiles = (
                world.platform_group.sprites() +
                world.breaking_platform_group.sprites() +
                world.hover_visible_platform_group.sprites() +
                world.moving_platform_group.sprites() +
                world.drawable_platform_group.sprites()
            )

            if self.first_frame:
                dy = 0
                self.vel_y = 0
                self.fall_speed = 0
                self.first_frame = False

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
                    break

            # Коллизии с BouncingPlatform
            for tile in world.bouncing_platform_group.sprites():
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

            # Монеты и двери
            collected = pygame.sprite.spritecollide(self, coin_group, True)
            if collected:
                self.coin_sound.play()
            self.coins_collected += len(collected)

            for door in door_group:
                if self.rect.colliderect(door.rect):
                    can_enter = True
                    # Если есть клон — проверяем дистанцию
                    if hasattr(world, 'clone') and world.clone:
                        dist = abs(self.rect.centerx - world.clone.rect.centerx)
                        if dist < 60:  # 60 — можно увеличить/уменьшить, под размер двери
                            can_enter = False
                    if can_enter and door.image == door.opened:
                        game_over = 1
                        # Если нужно — убиваем клона
                        if hasattr(world, 'clone') and world.clone:
                            world.clone.kill()
                            world.clone = None

            if self.rect.y > HEIGHT:
                game_over = -1

            # Обновляем клона
            if hasattr(world, 'clone') and world.clone:
                world.clone.update(keys, self.direction, self.jumped)


        # Обновление спрайта игрока
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

        # Превью рисуемых платформ
        if self.drawing_platform and self.platform_start_pos is not None and self.platform_end_pos is not None:
            start_x = min(self.platform_start_pos, self.platform_end_pos)
            end_x = max(self.platform_start_pos, self.platform_end_pos)
            height = (pygame.mouse.get_pos()[1] // TILE_SIZE) * TILE_SIZE
            pygame.draw.rect(screen, (200, 200, 200, 150), (start_x, height, end_x - start_x + TILE_SIZE, TILE_SIZE))

        return game_over