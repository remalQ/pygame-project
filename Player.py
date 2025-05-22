import pygame
from Const_Values import *
from Create_Maps import TILE_SIZE


class Player:
    def __init__(self, x, y, coin_sound, jump_sound):
        self.hitbox_width = 28
        self.hitbox_height = 90
        self.offset_x = (80 - self.hitbox_width) // 2
        self.coin_sound = coin_sound
        self.jump_sound = jump_sound
        self.reset(x, y)
        self.coins_collected = 0
        self.coin_image = pygame.image.load("Coins/Gold_1.png")
        self.coin_image = pygame.transform.scale(self.coin_image, (40, 40))

    def update(self, game_over, world, door_group, coin_group, screen):
        dx = 0
        dy = 0
        walk_cooldown = 3

        if game_over == 0:
            key = pygame.key.get_pressed()
            mouse_buttons = pygame.mouse.get_pressed()

            # Горизонтальный отскок
            if self.horizontal_bouncing:
                dx += self.horizontal_bounce_speed
                if self.horizontal_bounce_speed > 0:
                    self.horizontal_bounce_speed = max(0, self.horizontal_bounce_speed - self.horizontal_bounce_deceleration)
                else:
                    self.horizontal_bounce_speed = min(0, self.horizontal_bounce_speed + self.horizontal_bounce_deceleration)
                if self.horizontal_bounce_speed == 0:
                    self.horizontal_bouncing = False

            # Вертикальный отскок
            if self.vertical_bouncing:
                dy += self.vertical_bounce_speed
                if self.vertical_bounce_speed > 0:
                    self.vertical_bounce_speed = max(0, self.vertical_bounce_speed - self.vertical_bounce_deceleration)
                else:
                    self.vertical_bounce_speed = min(0, self.vertical_bounce_speed + self.vertical_bounce_deceleration)
                if self.vertical_bounce_speed == 0:
                    self.vertical_bouncing = False

            if not self.horizontal_bouncing:
                if key[pygame.K_a]:
                    dx -= 5
                    self.counter += 1
                    self.direction = -1
                    if not self.in_air and self.counter > walk_cooldown:
                        self.counter = 0
                        self.index = (self.index + 1) % len(self.images_left)
                        self.image = self.images_left[self.index]
                if key[pygame.K_d]:
                    dx += 5
                    self.counter += 1
                    self.direction = 1
                    if not self.in_air and self.counter > walk_cooldown:
                        self.counter = 0
                        self.index = (self.index + 1) % len(self.images_right)
                        self.image = self.images_right[self.index]

            if hasattr(world, 'allow_drawing') and world.allow_drawing:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_buttons[0]:
                    if not self.drawing_platform:
                        self.drawing_platform = True
                        self.platform_start_pos = (mouse_pos[0] // TILE_SIZE) * TILE_SIZE
                    self.platform_end_pos = (mouse_pos[0] // TILE_SIZE) * TILE_SIZE
                else:
                    if self.drawing_platform:
                        self.drawing_platform = False
                        if self.platform_start_pos and self.platform_end_pos:
                            start_x = min(self.platform_start_pos, self.platform_end_pos)
                            end_x = max(self.platform_start_pos, self.platform_end_pos)
                            for x in range(start_x, end_x + TILE_SIZE, TILE_SIZE):
                                world.add_drawable_platform(x, (mouse_pos[1] // TILE_SIZE) * TILE_SIZE)
                        self.platform_start_pos = None
                        self.platform_end_pos = None

            if key[pygame.K_SPACE] and not self.jumped and not self.in_air and not self.falling_mode:
                self.vel_y = -15
                self.jumped = True
                self.jump_sound.play()
                self.image = self.jump_image_right if self.direction == 1 else self.jump_image_left

            if not key[pygame.K_SPACE]:
                self.jumped = False

            if self.falling_mode:
                self.fall_speed += 0.5
                dy += self.fall_speed
                if self.fall_speed > 15:
                    self.fall_speed = 15
            elif not self.vertical_bouncing:
                self.vel_y += 1
                if self.vel_y > 10:
                    self.vel_y = 10
                dy += self.vel_y

            self.in_air = True

            all_platforms = (world.platform_group.sprites() +
                             world.breaking_platform_group.sprites() +
                             world.hover_visible_platform_group.sprites() +
                             world.moving_platform_group.sprites() +
                             world.drawable_platform_group.sprites())

            if self.first_frame:
                dy = 0
                self.vel_y = 0
                self.fall_speed = 0
                self.first_frame = False

            for tile in all_platforms:
                if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                    if dx > 0:
                        dx = tile.rect.left - self.rect.right
                    elif dx < 0:
                        dx = tile.rect.right - self.rect.left
                    self.vel_x = 0

                if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                    if self.vel_y >= 0 or self.fall_speed >= 0:
                        dy = tile.rect.top - self.rect.bottom
                        self.vel_y = 0
                        self.fall_speed = 0
                        self.in_air = False
                        self.falling_mode = False
                        if tile in world.breaking_platform_group:
                            if hasattr(tile, "start_disappear_timer") and not tile.is_disappeared:
                                tile.start_disappear_timer()
                    elif self.vel_y < 0 or self.fall_speed < 0:
                        dy = tile.rect.bottom - self.rect.top
                        self.vel_y = 0
                        self.fall_speed = 0

            if self.first_frame:
                for tile in all_platforms:
                    if tile.rect.colliderect(self.rect.x, self.rect.y + 1, self.rect.width, self.rect.height):
                        self.in_air = False
                        self.falling_mode = False
                        break

            for tile in world.bouncing_platform_group.sprites():
                if tile.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.rect.width, self.rect.height):
                    bounce_dx, bounce_dy = tile.apply_bounce(self)
                    dx += bounce_dx
                    dy += bounce_dy

            collected_coins = pygame.sprite.spritecollide(self, coin_group, True)
            if collected_coins:
                self.coin_sound.play()
            self.coins_collected += len(collected_coins)

            for door in door_group:
                if self.rect.colliderect(door.rect):
                    if door.image == door.opened:
                        game_over = 1
                    else:
                        if self.rect.right > door.rect.left and self.direction == 1:
                            dx = door.rect.left - self.rect.right
                        elif self.rect.left < door.rect.right and self.direction == -1:
                            dx = door.rect.right - self.rect.left

            if self.rect.y > HEIGHT:
                game_over = -1

            self.rect.x += dx
            self.rect.y += dy

        screen.blit(self.image, (self.rect.x - self.offset_x, self.rect.bottom - self.image.get_height()))

        if self.drawing_platform and self.platform_start_pos and self.platform_end_pos:
            start_x = min(self.platform_start_pos, self.platform_end_pos)
            end_x = max(self.platform_start_pos, self.platform_end_pos)
            height = (pygame.mouse.get_pos()[1] // TILE_SIZE) * TILE_SIZE
            pygame.draw.rect(screen, (200, 200, 200, 150),
                             (start_x, height, end_x - start_x + TILE_SIZE, TILE_SIZE))

        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0

        for num in range(1, 5):
            img_right = pygame.image.load(f'Assets/frame{num}.png').convert_alpha()
            img_right = pygame.transform.scale(img_right, (80, 90))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.jump_image_right = pygame.image.load('Assets/frame_jump.png').convert_alpha()
        self.jump_image_right = pygame.transform.scale(self.jump_image_right, (80, 90))
        self.jump_image_left = pygame.transform.flip(self.jump_image_right, True, False)

        self.direction = 1
        self.image = self.images_right[self.index]

        self.rect = pygame.Rect(x, y, self.hitbox_width, self.hitbox_height)

        self.vel_y = 0
        self.vel_x = 0
        self.jumped = False
        self.in_air = True
        self.drawing_platform = False
        self.platform_start_pos = None
        self.platform_end_pos = None
        self.falling_mode = False
        self.fall_speed = 0
        self.first_frame = True

        self.vertical_bouncing = False
        self.horizontal_bouncing = False
        self.vertical_bounce_speed = 0
        self.horizontal_bounce_speed = 0
        self.vertical_bounce_deceleration = 0
        self.horizontal_bounce_deceleration = 0

    def start_falling(self):
        self.falling_mode = True
        self.fall_speed = 3

    def start_vertical_bounce(self, initial_speed, deceleration):
        self.vertical_bounce_speed = initial_speed
        self.vertical_bounce_deceleration = deceleration
        self.vertical_bouncing = True

    def start_horizontal_bounce(self, initial_speed, deceleration):
        self.horizontal_bounce_speed = initial_speed
        self.horizontal_bounce_deceleration = deceleration
        self.horizontal_bouncing = True