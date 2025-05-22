# Player.py
import pygame
from Const_Values import DEFAULT_GRAVITY, HEIGHT
from Create_Maps import TILE_SIZE

class Player:
    def __init__(self, x, y, coin_sound, jump_sound):
        # Размер хитбокса и сдвиг для отрисовки
        self.hitbox_width = 28
        self.hitbox_height = 90
        self.offset_x = (80 - self.hitbox_width) // 2

        # Звуки и монетки
        self.coin_sound = coin_sound
        self.jump_sound = jump_sound
        self.coins_collected = 0
        self.coin_image = pygame.image.load("Coins/Gold_1.png").convert_alpha()
        self.coin_image = pygame.transform.scale(self.coin_image, (40, 40))

        # Режим рисования платформ (уровень 3)
        self.drawing_platform = False
        self.platform_start_pos = None
        self.platform_end_pos = None

        # Режим падения
        self.falling_mode = False
        self.fall_speed = 0

        # Параметры «отскока»
        self.vertical_bouncing = False
        self.horizontal_bouncing = False
        self.vertical_bounce_speed = 0
        self.horizontal_bounce_speed = 0
        self.vertical_bounce_deceleration = 0
        self.horizontal_bounce_deceleration = 0

        # Параметры зон-эффектов
        self.jump_multiplier = 1.0
        self.gravity = DEFAULT_GRAVITY
        self.can_pass_walls = False

        # Базовые константы
        self.base_jump_speed = 15
        self.max_fall_speed = 15

        # Горизонтальная скорость от предыдущих отталкиваний
        self.vel_x = 0

        # Флаг первого кадра
        self.first_frame = True

        # Загрузка спрайтов и инициализация
        self.reset(x, y)


    def reset(self, x, y):
        """Сбрасывает состояние игрока."""
        # Анимации
        self.images_right = []
        self.images_left  = []
        for num in range(1, 5):
            img = pygame.image.load(f'Assets/frame{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (80, 90))
            self.images_right.append(img)
            self.images_left.append(pygame.transform.flip(img, True, False))
        self.jump_image_right = pygame.image.load('Assets/frame_jump.png').convert_alpha()
        self.jump_image_right = pygame.transform.scale(self.jump_image_right, (80, 90))
        self.jump_image_left  = pygame.transform.flip(self.jump_image_right, True, False)

        self.direction = 1
        self.image     = self.images_right[0]
        self.index     = 0
        self.counter   = 0

        # Позиция и хитбокс
        self.rect = pygame.Rect(x, y, self.hitbox_width, self.hitbox_height)

        # Вертикальные параметры
        self.vel_y = 0
        self.jumped = False
        self.in_air = True

        # Сброс режимов
        self.drawing_platform   = False
        self.platform_start_pos = None
        self.platform_end_pos   = None
        self.falling_mode       = False
        self.fall_speed         = 0
        self.first_frame        = True

        # Сброс зон-эффектов
        self.jump_multiplier = 1.0
        self.gravity         = DEFAULT_GRAVITY
        self.can_pass_walls  = False

        # Сброс отскока
        self.vertical_bouncing           = False
        self.horizontal_bouncing         = False
        self.vertical_bounce_speed       = 0
        self.horizontal_bounce_speed     = 0
        self.vertical_bounce_deceleration   = 0
        self.horizontal_bounce_deceleration = 0


    def start_vertical_bounce(self, initial_speed, deceleration):
        """Запускает отскок по Y."""
        self.vertical_bounce_speed       = initial_speed
        self.vertical_bounce_deceleration = deceleration
        self.vertical_bouncing           = True


    def start_horizontal_bounce(self, initial_speed, deceleration):
        """Запускает отскок по X."""
        self.horizontal_bounce_speed       = initial_speed
        self.horizontal_bounce_deceleration = deceleration
        self.horizontal_bouncing           = True


    def start_falling(self):
        """Включает режим свободного падения."""
        self.falling_mode = True
        self.fall_speed   = 3


    def update(self, game_over, world, door_group, coin_group, screen):
        """
        Основной апдейт игрока. Возвращает новое значение game_over.
        """
        dx = 0
        dy = 0
        walk_cooldown = 3

        # helper: True, если эта плитка в зоне ghost_mode
        def tile_in_ghost_zone(tile):
            for z in world.zones:
                if z['effect'] == 'ghost_mode':
                    if pygame.Rect(z['x'], z['y'], z['w'], z['h']).colliderect(tile.rect):
                        return True
            return False

        if game_over == 0:
            key = pygame.key.get_pressed()
            mouse_buttons = pygame.mouse.get_pressed()

            # --- рисуем платформы (ур.3) ---
            if hasattr(world, 'allow_drawing') and world.allow_drawing:
                mpos = pygame.mouse.get_pos()
                if mouse_buttons[0]:
                    if not self.drawing_platform:
                        self.drawing_platform   = True
                        self.platform_start_pos = (mpos[0] // TILE_SIZE) * TILE_SIZE
                    self.platform_end_pos = (mpos[0] // TILE_SIZE) * TILE_SIZE
                else:
                    if self.drawing_platform:
                        self.drawing_platform = False
                        if self.platform_start_pos is not None and self.platform_end_pos is not None:
                            start_x = min(self.platform_start_pos, self.platform_end_pos)
                            end_x   = max(self.platform_start_pos, self.platform_end_pos)
                            y_tile  = (mpos[1] // TILE_SIZE) * TILE_SIZE
                            for x in range(start_x, end_x + TILE_SIZE, TILE_SIZE):
                                world.add_drawable_platform(x, y_tile)
                        self.platform_start_pos = None
                        self.platform_end_pos   = None

            # --- отскок ---
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

            # --- скольжение по X ---
            if abs(self.vel_x) > 0:
                dx += self.vel_x
                self.vel_x *= 0.9

            # --- движение и гравитация ---
            if self.falling_mode:
                self.fall_speed += 0.5
                dy += self.fall_speed
                if self.fall_speed > self.max_fall_speed:
                    self.fall_speed = self.max_fall_speed
            else:
                # ходьба
                if key[pygame.K_a]:
                    dx -= 5
                    self.counter += 1
                    self.direction = -1
                    if not self.in_air and self.counter > walk_cooldown:
                        self.counter = 0
                        self.index   = (self.index + 1) % len(self.images_left)
                        self.image   = self.images_left[self.index]
                if key[pygame.K_d]:
                    dx += 5
                    self.counter += 1
                    self.direction = 1
                    if not self.in_air and self.counter > walk_cooldown:
                        self.counter = 0
                        self.index   = (self.index + 1) % len(self.images_right)
                        self.image   = self.images_right[self.index]

                # прыжок с учётом зоны
                if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
                    self.vel_y = -self.base_jump_speed * self.jump_multiplier
                    self.jumped = True
                    self.jump_sound.play()
                    self.image = (self.jump_image_right if self.direction == 1
                                  else self.jump_image_left)
                if not key[pygame.K_SPACE]:
                    self.jumped = False

                # спрайт в полёте/стоянии
                if self.in_air:
                    self.image = (self.jump_image_right if self.direction == 1
                                  else self.jump_image_left)
                elif not key[pygame.K_a] and not key[pygame.K_d]:
                    self.counter = 0
                    self.index   = 0
                    self.image   = (self.images_right[self.index]
                                    if self.direction == 1
                                    else self.images_left[self.index])

                # гравитация
                self.vel_y += self.gravity
                if self.vel_y > self.max_fall_speed:
                    self.vel_y = self.max_fall_speed
                dy += self.vel_y

            # --- коллизии ---
            self.in_air = True
            all_platforms = (
                world.platform_group.sprites() +
                world.breaking_platform_group.sprites() +
                world.hover_visible_platform_group.sprites() +
                world.moving_platform_group.sprites() +
                world.drawable_platform_group.sprites()
            )

            # первый кадр — сброс dy
            if self.first_frame:
                dy = 0
                self.vel_y = 0
                self.fall_speed = 0
                self.first_frame = False

            # горизонтальные
            for tile in all_platforms:
                if self.can_pass_walls and tile_in_ghost_zone(tile):
                    continue
                if tile.rect.colliderect(self.rect.x + dx,
                                         self.rect.y,
                                         self.rect.width,
                                         self.rect.height):
                    if dx > 0:
                        dx = tile.rect.left - self.rect.right
                    else:
                        dx = tile.rect.right - self.rect.left
                    self.vel_x = 0

            # вертикальные
            for tile in all_platforms:
                if self.can_pass_walls and tile_in_ghost_zone(tile):
                    continue
                if tile.rect.colliderect(self.rect.x,
                                         self.rect.y + dy,
                                         self.rect.width,
                                         self.rect.height):
                    if self.vel_y >= 0 or self.fall_speed >= 0:
                        dy = tile.rect.top - self.rect.bottom
                        self.vel_y = 0
                        self.fall_speed = 0
                        self.in_air = False
                        self.falling_mode = False
                        if tile in world.breaking_platform_group:
                            if hasattr(tile, "start_disappear_timer") and not tile.is_disappeared:
                                tile.start_disappear_timer()
                    else:
                        dy = tile.rect.bottom - self.rect.top
                        self.vel_y = 0
                        self.fall_speed = 0

            # bouncing-платформы
            for tile in world.bouncing_platform_group.sprites():
                if self.can_pass_walls and tile_in_ghost_zone(tile):
                    continue
                if tile.rect.colliderect(self.rect.x + dx,
                                         self.rect.y + dy,
                                         self.rect.width,
                                         self.rect.height):
                    bx, by = tile.apply_bounce(self)
                    dx += bx
                    dy += by

            # --- монетки ---
            collected = pygame.sprite.spritecollide(self, coin_group, True)
            if collected:
                self.coin_sound.play()
            self.coins_collected += len(collected)

            # --- двери и выход ---
            for door in door_group:
                if self.rect.colliderect(door.rect):
                    if door.image == door.opened:
                        game_over = 1
                    else:
                        if self.rect.right > door.rect.left and self.direction == 1:
                            dx = door.rect.left - self.rect.right
                        elif self.rect.left < door.rect.right and self.direction == -1:
                            dx = door.rect.right - self.rect.left

            # падение за экран
            if self.rect.y > HEIGHT:
                game_over = -1

            # применяем
            self.rect.x += dx
            self.rect.y += dy

        # отрисовка
        screen.blit(self.image,
                    (self.rect.x - self.offset_x,
                     self.rect.bottom - self.image.get_height()))

        # превью рисуемых платформ
        if self.drawing_platform and self.platform_start_pos is not None and self.platform_end_pos is not None:
            start_x = min(self.platform_start_pos, self.platform_end_pos)
            end_x   = max(self.platform_start_pos, self.platform_end_pos)
            height  = (pygame.mouse.get_pos()[1] // TILE_SIZE) * TILE_SIZE
            pygame.draw.rect(screen, (200, 200, 200, 150),
                             (start_x, height,
                              end_x - start_x + TILE_SIZE, TILE_SIZE))

        return game_over
