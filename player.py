import pygame
import sys
from const_value import *
from os import path, listdir
import pickle

# Класс кнопки
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

# Класс меню выбора уровня
class LevelMenu():
    def __init__(self, total_levels):
        self.buttons = []
        self.total_levels = total_levels

    def show(self, screen):
        menu_active = True
        self.buttons = []
        for i in range(1, self.total_levels + 1):
            button = Button(f"Уровень {i}", WIDTH // 2, HEIGHT // 2 - 100 + i * 50, GRAY, WHITE)
            self.buttons.append(button)

        while menu_active:
            screen.fill(BLACK)
            for button in self.buttons:
                button.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        if button.is_clicked(pygame.mouse.get_pos()):
                            return i + 1  # Возвращаем выбранный уровень

            pygame.display.flip()

# Класс игрока
class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over, world, door_group, screen):
        dx = 0
        dy = 0
        walk_cooldown = 5

        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
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

# Класс двери
class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load('img/door.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect(topleft=(x, y))

# Класс мира (уровня)
class World():
    def __init__(self, data, door_group):
        self.tile_list = []
        self.door_group = door_group
        block_img = pygame.image.load('img/platform1.png')

        for row_count, row in enumerate(data):
            for col_count, tile in enumerate(row):
                if tile == 1:
                    img = pygame.transform.scale(block_img, (tile_size, tile_size))
                    img_rect = img.get_rect(topleft=(col_count * tile_size, row_count * tile_size))
                    self.tile_list.append((img, img_rect))
                if tile == 2:
                    door = Door(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    self.door_group.add(door)

    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
        self.door_group.draw(screen)

# Класс игры
class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Платформер')
        self.clock = pygame.time.Clock()
        self.door_group = pygame.sprite.Group()  # Инициализация группы дверей
        self.total_levels = len([f for f in listdir('maps') if f.startswith('map') and f.endswith('.pkl')])
        self.level = 1
        self.world_data = []
        self.load_level(self.level)
        self.player = Player(100, HEIGHT - 130)
        self.game_over = 0

    def load_level(self, level):
        if path.exists(f'maps/map{level}.pkl'):
            with open(f'maps/map{level}.pkl', 'rb') as pickle_in:
                self.world_data = pickle.load(pickle_in)
        self.world = World(self.world_data, self.door_group)  # Передаем door_group в World

    def reset_level(self, level):
        self.player.reset(100, HEIGHT - 130)
        self.door_group.empty()  # Очищаем группу дверей перед загрузкой нового уровня
        self.load_level(level)

    def show_main_menu(self):
        menu_active = True
        start_button = Button("Начать игру", WIDTH // 2, HEIGHT // 2 - 50, GRAY, WHITE)
        exit_button = Button("Выход", WIDTH // 2, HEIGHT // 2 + 50, GRAY, WHITE)

        while menu_active:
            self.screen.fill(BLACK)
            start_button.draw(self.screen)
            exit_button.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.is_clicked(pygame.mouse.get_pos()):
                        level_menu = LevelMenu(self.total_levels)
                        selected_level = level_menu.show(self.screen)
                        if selected_level:
                            self.level = selected_level
                            self.reset_level(self.level)
                            menu_active = False
                    if exit_button.is_clicked(pygame.mouse.get_pos()):
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()

    def show_pause_menu(self):
        pause_active = True
        continue_button = Button("Продолжить", WIDTH // 2, HEIGHT // 2 - 50, GRAY, WHITE)
        main_menu_button = Button("Выход в меню", WIDTH // 2, HEIGHT // 2 + 50, GRAY, WHITE)

        while pause_active:
            self.screen.fill(BLACK)
            continue_button.draw(self.screen)
            main_menu_button.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.is_clicked(pygame.mouse.get_pos()):
                        pause_active = False
                    if main_menu_button.is_clicked(pygame.mouse.get_pos()):
                        self.show_main_menu()
                        pause_active = False

            pygame.display.flip()

    def show_game_completed_screen(self):
        completed_active = True
        main_menu_button = Button("Выход в меню", WIDTH // 2, HEIGHT // 2, GRAY, WHITE)

        while completed_active:
            self.screen.fill(BLACK)
            font = pygame.font.SysFont(None, 60)
            text = font.render("Игра пройдена!", True, WHITE)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))
            main_menu_button.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if main_menu_button.is_clicked(pygame.mouse.get_pos()):
                        self.show_main_menu()
                        completed_active = False

            pygame.display.flip()

    def run(self):
        self.show_main_menu()

        running = True
        while running:
            self.clock.tick(FPS)
            self.screen.fill((255, 255, 255))

            self.world.draw(self.screen)
            self.game_over = self.player.update(self.game_over, self.world, self.door_group, self.screen)

            if self.game_over == 1:
                if self.level < self.total_levels:
                    self.level += 1
                    self.reset_level(self.level)
                    self.game_over = 0
                else:
                    self.show_game_completed_screen()
                    self.game_over = 0

            if self.game_over == -1:
                self.reset_level(self.level)
                self.game_over = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.show_pause_menu()

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
