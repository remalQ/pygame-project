# Game.py
import sys
import pickle
from pygame.sprite import Group
from Const_Values import *
import os
from Player import Player
from Button import Button
from World import World
from Menus.Level_Menu import LevelMenu
from RecordsDB import RecordsDB
from Menus.LeaderboardMenu import LeaderboardMenu
from Menus.SettingsMenu import SettingsMenu
from Menus.HelpMenu import HelpMenu
import pygame

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Mind flip')
        self.clock = pygame.time.Clock()
        self.door_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()

        self.music_file = "Sounds/back.mp3"
        self.music_playing = False
        self.music_position = 0
        self.sound_volume = 0.5

        try:
            self.coin_sound = pygame.mixer.Sound("Sounds/coin.wav")
            self.jump_sound = pygame.mixer.Sound("Sounds/jump.wav")
            self.coin_sound.set_volume(self.sound_volume)
            self.jump_sound.set_volume(self.sound_volume)
        except pygame.error as e:
            print(f"Ошибка загрузки звуковых эффектов: {e}")

        self.player = Player(100, HEIGHT - 130, self.coin_sound, self.jump_sound)

        level_files = [f for f in os.listdir('Maps') if f.endswith('.pkl')]
        def extract_level_number(filename):
            try:
                return int(filename.split('.')[0].replace('level', ''))
            except ValueError:
                return 0
        level_files.sort(key=extract_level_number)
        self.total_levels = len(level_files)

        self.level = 1
        self.world_data = []
        if self.total_levels > 0:
            self.load_level(self.level)
        else:
            self.world_data = {'grid': [], 'texts': []}
            self.world = World(self.world_data, self.door_group, self.coin_group, self.player)
        self.game_over = 0
        self.records_db = RecordsDB()
        self.start_time = 0
        self.current_time = 0
        self.settings_menu = SettingsMenu(self)
        self.help_menu = HelpMenu()
        self.level_menu = LevelMenu(self.total_levels)
        self.stop_broken = False

    def set_sound_volume(self, volume):
        self.sound_volume = volume
        if self.coin_sound:
            self.coin_sound.set_volume(self.sound_volume)
        if self.jump_sound:
            self.jump_sound.set_volume(self.sound_volume)

    def reset_level(self, level):
        self.player.coins_collected = 0
        self.game_over = 0
        self.start_time = pygame.time.get_ticks()

        if level == 3:
            self.player.reset(100, -100)
            self.player.start_falling()
            self.world.allow_drawing = True
            self.world.reset_drawable_platforms()
        else:
            y_position = HEIGHT - 130
            all_platforms = (self.world.platform_group.sprites() +
                             self.world.breaking_platform_group.sprites() +
                             self.world.hover_visible_platform_group.sprites() +
                             self.world.moving_platform_group.sprites() +
                             self.world.drawable_platform_group.sprites())
            for platform in all_platforms:
                if (platform.rect.left <= 100 <= platform.rect.right and
                        platform.rect.top <= HEIGHT and platform.rect.top >= HEIGHT - 200):
                    y_position = platform.rect.top - self.player.hitbox_height
                    break
            self.player.reset(100, y_position)
            self.world.allow_drawing = False

        self.load_level(level)

        if level != 4 or not self.stop_broken:
            self.stop_broken = False

    def load_level(self, level):
        self.door_group = Group()
        self.coin_group = Group()

        level_path = f'Maps/level{level}.pkl'
        if os.path.exists(level_path):
            try:
                with open(level_path, 'rb') as pickle_in:
                    self.world_data = pickle.load(pickle_in)
                if not isinstance(self.world_data, (list, dict)):
                    raise ValueError("Ошибка: загруженные данные уровня не являются списком или словарем!")
            except Exception as e:
                print(f"Ошибка загрузки уровня: {e}")
                self.world_data = {'grid': [], 'texts': []}
        else:
            self.world_data = {'grid': [], 'texts': []}

        self.world = World(self.world_data, self.door_group, self.coin_group, self.player)
        if level == 3:
            self.world.allow_drawing = True
        else:
            self.world.allow_drawing = False

    def start_music(self):
        if not self.music_playing:
            try:
                pygame.mixer.music.load(self.music_file)
                pygame.mixer.music.play(-1, start=self.music_position / 1000)
                self.music_playing = True
            except pygame.error as e:
                print(f"Ошибка загрузки музыки: {e}")

    def stop_music(self):
        if self.music_playing:
            self.music_position = pygame.mixer.music.get_pos()
            pygame.mixer.music.stop()
            self.music_playing = False

    def reset_music(self):
        self.stop_music()
        self.music_position = 0

    def show_main_menu(self):
        self.reset_music()
        if self.level == 4:
            self.stop_broken = True
        menu_active = True
        start_button = Button("Начать игру", WIDTH // 2, HEIGHT // 2 - 200, GRAY, WHITE)
        settings_button = Button("Настройки", WIDTH // 2, HEIGHT // 2 - 100, GRAY, WHITE)
        help_button = Button("Помощь", WIDTH // 2, HEIGHT // 2, GRAY, WHITE)
        leaderboard_button = Button("Таблица лидеров", WIDTH // 2, HEIGHT // 2 + 100, GRAY, WHITE)
        exit_button = Button("Выход", WIDTH // 2, HEIGHT // 2 + 200, GRAY, WHITE)

        while menu_active:
            self.screen.fill(BLACK)
            start_button.draw(self.screen)
            leaderboard_button.draw(self.screen)
            exit_button.draw(self.screen)
            settings_button.draw(self.screen)
            help_button.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.is_clicked(pygame.mouse.get_pos()):
                        selected_level = self.level_menu.show(self.screen)
                        if selected_level:
                            self.level = selected_level
                            self.reset_level(self.level)
                            self.start_time = pygame.time.get_ticks()
                            self.start_music()
                            pygame.event.clear()
                            menu_active = False
                            return
                    if leaderboard_button.is_clicked(pygame.mouse.get_pos()):
                        leaderboard_menu = LeaderboardMenu(self.records_db)
                        leaderboard_menu.show(self.screen)
                    if settings_button.is_clicked(pygame.mouse.get_pos()):
                        self.settings_menu.show(self.screen)
                    if help_button.is_clicked(pygame.mouse.get_pos()):
                        self.help_menu.show(self.screen)
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
            font = pygame.font.Font("Fonts/Monocraft.otf", 40)
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

    def check_and_save_record(self):
        if self.game_over == 1:
            completion_time = self.current_time
            player_name = "Player"
            self.records_db.add_record(player_name, completion_time, self.level)

    def run(self):
        self.show_main_menu()
        running = True

        while running:
            self.clock.tick(FPS)
            self.screen.fill((255, 255, 255))

            if self.game_over == 0:
                self.current_time = (pygame.time.get_ticks() - self.start_time) / 1000

            self.world.draw(self.screen)

            self.game_over = self.player.update(self.game_over, self.world, self.door_group, self.coin_group, self.screen)

            self.world.breaking_platform_group.update()
            self.world.hover_visible_platform_group.update()
            self.world.update()

            if self.game_over == 1:
                self.check_and_save_record()
                self.level_menu.unlock_next_level(self.level)
                if self.level == 4 and not self.stop_broken:
                    self.reset_level(self.level)
                    self.game_over = 0
                    self.start_time = pygame.time.get_ticks()
                elif self.level < self.total_levels:
                    self.level += 1
                    self.reset_level(self.level)
                    self.game_over = 0
                    self.start_time = pygame.time.get_ticks()
                else:
                    self.show_game_completed_screen()
                    self.game_over = 0

            if self.game_over == -1:
                self.reset_level(self.level)
                self.game_over = 0
                self.start_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.show_pause_menu()

            pygame.display.flip()

        pygame.quit()