import sys
import pickle
from Const_Values import *
from os import path, listdir
from Player import Player
from Button import Button
from World import World
from Level_Menu import LevelMenu


class Game:
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


