import sys
import pickle
from pygame.sprite import Group
from Const_Values import *
import os
from Player import Player
from Button import Button
from World import World
from Level_Menu import LevelMenu
from RecordsDB import RecordsDB
from LeaderboardMenu import LeaderboardMenu


"""
Класс Game

Отвечает за управление игровым процессом: загрузку уровней, отображение меню, обработку событий и обновление состояния игры.
"""


class Game:
    ## \brief Конструктор класса
    #
    # Инициализирует основные параметры игры, загружает первый уровень.
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Платформер')
        self.clock = pygame.time.Clock()
        self.door_group = pygame.sprite.Group()

        # Получаем список всех файлов уровней
        level_files = [f for f in os.listdir('maps') if f.endswith('.pkl')]

        # Безопасная сортировка по номеру уровня
        def extract_level_number(filename):
            try:
                # Удаляем расширение и префикс 'level', затем преобразуем в число
                return int(filename.split('.')[0].replace('level', ''))
            except ValueError:
                return 0  # Для файлов с некорректными именами

        level_files.sort(key=extract_level_number)
        self.total_levels = len(level_files)

        self.level = 1
        self.world_data = []
        if self.total_levels > 0:
            self.load_level(self.level)
        else:
            print("Нет доступных уровней в папке maps/")
            self.world_data = []
        self.player = Player(100, HEIGHT - 130)
        self.game_over = 0
        self.records_db = RecordsDB()
        self.start_time = 0
        self.current_time = 0

    def reset_level(self, level):
        """Сбрасывает уровень и позицию игрока"""
        self.load_level(level)
        self.player.reset(100, HEIGHT - 130)
        self.game_over = 0
        self.start_time = pygame.time.get_ticks()

    ## \brief Загрузка уровня
    #
    # Загружает данные уровня из файла.
    # @param level Номер загружаемого уровня.
    def load_level(self, level):
        level_path = f'maps/map{level}.pkl'  # Исправлено для соответствия именам файлов
        self.door_group = Group()
        # self.spike_group = Group()
        # self.coin_group = Group()

        if os.path.exists(level_path):
            try:
                with open(level_path, 'rb') as pickle_in:
                    self.world_data = pickle.load(pickle_in)

                if not isinstance(self.world_data, list):
                    raise ValueError("Ошибка: загруженные данные уровня не являются списком!")

                # Создаем мир
                self.world = World(self.world_data, self.door_group)
                print(f"Уровень {level} успешно загружен!")
            except Exception as e:
                print(f"Ошибка загрузки уровня {level}: {e}")
                self.world_data = []
                self.world = World(self.world_data, self.door_group)  # Пустой мир
        else:
            print(f"Файл {level_path} не найден!")

    ## \brief Главное меню
    #
    # Отображает главное меню с возможностью начать игру или выйти.
    def show_main_menu(self):
        menu_active = True
        start_button = Button("Начать игру", WIDTH // 2, HEIGHT // 2 - 100, GRAY, WHITE)
        leaderboard_button = Button("Таблица лидеров", WIDTH // 2, HEIGHT // 2, GRAY, WHITE)
        exit_button = Button("Выход", WIDTH // 2, HEIGHT // 2 + 100, GRAY, WHITE)

        while menu_active:
            self.screen.fill(BLACK)
            start_button.draw(self.screen)
            leaderboard_button.draw(self.screen)
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
                            self.start_time = pygame.time.get_ticks()  # Запуск таймера
                            menu_active = False
                    if leaderboard_button.is_clicked(pygame.mouse.get_pos()):
                        leaderboard_menu = LeaderboardMenu(self.records_db)
                        leaderboard_menu.show(self.screen)
                    if exit_button.is_clicked(pygame.mouse.get_pos()):
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()

    ## \brief Меню паузы
    #
    # Отображает меню паузы с возможностью продолжить игру или выйти в главное меню.
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

    ## \brief Экран завершения игры
    #
    # Отображает экран завершения игры, если все уровни пройдены.
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

    def check_and_save_record(self):
        if self.game_over == 1:  # Если уровень пройден
            completion_time = self.current_time
            player_name = "Player"  # Можно запросить имя игрока или использовать сохраненное

            # Сохраняем рекорд
            self.records_db.add_record(player_name, completion_time, self.level)

    ## \brief Основной цикл игры
    #
    # Запускает игровой процесс, обрабатывает события и обновляет экран.
    def run(self):
        self.show_main_menu()
        running = True

        while running:
            self.clock.tick(FPS)
            self.screen.fill((255, 255, 255))

            if self.game_over == 0:
                self.current_time = (pygame.time.get_ticks() - self.start_time) / 1000  # В секундах

            if self.world:  # Проверяем, инициализирован ли world
                self.world.draw(self.screen)  # Отрисовываем мир
            self.game_over = self.player.update(self.game_over, self.world, self.door_group, self.screen)

            if self.game_over == 1:
                self.check_and_save_record()
                if self.level < self.total_levels:
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
