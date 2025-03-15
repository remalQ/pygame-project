import pygame
import sys
from const_value import *
from os import path
import pickle

restart_img = pygame.image.load('img/play_btn.png')
start_img = pygame.image.load('img/play_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')

class Button():
    def __init__(self, text, x, y, color, hover_color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont(None, 40)
        self.rect = pygame.Rect(x - 100, y - 25, 200, 50)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surf = self.font.render(self.text, True, BLACK)
        screen.blit(text_surf, (self.x - text_surf.get_width() // 2, self.y - text_surf.get_height() // 2))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    @staticmethod
    def show_main_menu():
        menu_active = True
        start_button = Button("Начать игру", WIDTH // 2, HEIGHT // 2 - 50, GRAY, WHITE)
        exit_button = Button("Выход", WIDTH // 2, HEIGHT // 2 + 50, GRAY, WHITE)

        while menu_active:
            screen.fill(BLACK)
            start_button.draw(screen)
            exit_button.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.is_clicked(pygame.mouse.get_pos()):
                        menu_active = False  # Переход к игре
                    if exit_button.is_clicked(pygame.mouse.get_pos()):
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()

def reset_level(level):
    player.reset(100, HEIGHT - 130)
    door_group.empty()
    if path.exists(f'maps/map{level}.pkl'):
        pickle_in = open(f'maps/map{level}.pkl', 'rb')
        world_data = pickle.load(pickle_in)
    world = Game(world_data)
    return world

# Класс Игрока
class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5

        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            self.in_air = True
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

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
        for num in range(1, 6):
            img_right = pygame.image.load(f'img/frame{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 60))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

class Game():
    def __init__(self, data):
        self.tile_list = []
        block_img = pygame.image.load('img/block.png')

        for row_count, row in enumerate(data):
            for col_count, tile in enumerate(row):
                if tile == 1:
                    img = pygame.transform.scale(block_img, (tile_size, tile_size))
                    img_rect = img.get_rect(topleft=(col_count * tile_size, row_count * tile_size))
                    self.tile_list.append((img, img_rect))
                if tile == 2:
                    door = Door(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    door_group.add(door)

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load('img/door.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect(topleft=(x, y))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Платформер')
clock = pygame.time.Clock()
door_group = pygame.sprite.Group()

game_over = 0
level = 1
world_data = []
if path.exists(f'maps/map{level}.pkl'):
    with open(f'maps/map{level}.pkl', 'rb') as pickle_in:
        world_data = pickle.load(pickle_in)

world = Game(world_data)
Button.show_main_menu()
player = Player(100, HEIGHT - 130)

running = True
while running:
    clock.tick(FPC)
    screen.fill((0, 0, 0))

    world.draw()
    door_group.draw(screen)  # Добавлена отрисовка двери
    game_over = player.update(game_over)

    if game_over == 1:
        level += 1
        world = reset_level(level)
        game_over = 0
    if game_over == -1:
        world = reset_level(level)
        game_over = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
