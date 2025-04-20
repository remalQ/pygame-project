"""@package Player
Класс игрока
"""
import pygame
from Const_Values import *
from Create_Maps import TILE_SIZE


class Player:
    def __init__(self, x, y):
        self.reset(x, y)
        self.coins_collected = 0
        self.coin_image = pygame.image.load("Coins/Gold_1.png")
        self.coin_image = pygame.transform.scale(self.coin_image, (40, 40))

    def update_hitbox(self):
        """Обновляет хитбокс по текущему изображению, сужая его по ширине на 30px (по 15px с каждой стороны)"""
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(-20, 0)
        self.rect.center = center

    def update(self, game_over, world, door_group, coin_group, screen):
        dx = 0
        dy = 0
        walk_cooldown = 3

        if game_over == 0:
            key = pygame.key.get_pressed()

            if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
                self.vel_y = -15
                self.jumped = True
                self.image = self.jump_image_right if self.direction == 1 else self.jump_image_left
                self.update_hitbox()

            if not key[pygame.K_SPACE]:
                self.jumped = False

            if key[pygame.K_a]:
                dx -= 5
                self.counter += 1
                self.direction = -1
                if not self.in_air and self.counter > walk_cooldown:
                    self.counter = 0
                    self.index = (self.index + 1) % len(self.images_left)
                    self.image = self.images_left[self.index]
                    self.update_hitbox()

            if key[pygame.K_d]:
                dx += 5
                self.counter += 1
                self.direction = 1
                if not self.in_air and self.counter > walk_cooldown:
                    self.counter = 0
                    self.index = (self.index + 1) % len(self.images_right)
                    self.image = self.images_right[self.index]
                    self.update_hitbox()

            if self.in_air:
                self.image = self.jump_image_right if self.direction == 1 else self.jump_image_left
                self.update_hitbox()
            elif not key[pygame.K_a] and not key[pygame.K_d]:
                self.counter = 0
                self.index = 0
                self.image = self.images_right[self.index] if self.direction == 1 else self.images_left[self.index]
                self.update_hitbox()

            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            self.in_air = True
            for tile in world.platform_group.sprites() + world.breaking_platform_group.sprites() \
                    + world.hover_visible_platform_group.sprites():
                if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                    dx = 0

                if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                    if self.vel_y < 0:
                        dy = tile.rect.bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile.rect.top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False
                        self.image = self.images_right[self.index] if self.direction == 1 else self.images_left[self.index]
                        self.update_hitbox()

                        if tile in world.breaking_platform_group:
                            if hasattr(tile, "start_disappear_timer") and not tile.is_disappeared:
                                tile.start_disappear_timer()

            collected_coins = pygame.sprite.spritecollide(self, coin_group, True)
            self.coins_collected += len(collected_coins)

            if pygame.sprite.spritecollide(self, door_group, False):
                game_over = 1

            if self.rect.y > HEIGHT:
                game_over = -1

            self.rect.x += dx
            self.rect.y += dy

        screen.blit(self.image, self.rect)
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
        self.rect = self.image.get_rect()
        self.rect.center = (x + self.image.get_width() // 2, y + self.image.get_height() // 2)

        self.vel_y = 0
        self.jumped = False
        self.in_air = True
