import sys
from Button import *
from Player import *
from Create_Levels import *


# Основной класс игры
class Game:
    def __init__(self):
        self.player = Player()
        self.platforms = pygame.sprite.Group()
        self.door = None
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # Уровни
        self.levels = [
            level_1,  # Уровень 1
            level_2,  # Уровень 2
        ]
        self.current_level = 0
        self.load_level(self.current_level)

        self.level_complete = False
        self.paused = False
        self.game_over = False  # Флаг для отслеживания проигрыша
        self.sound_enabled = True
        self.volume = 0.5

    def load_level(self, level_index):
        # Загружаем уровень
        self.platforms.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)

        platforms, door = self.levels[level_index].get_objects()
        for platform in platforms:
            self.platforms.add(platform)
            self.all_sprites.add(platform)
        self.door = door
        self.all_sprites.add(self.door)

        # Сбрасываем состояние игрока
        self.player.rect.topleft = (50, HEIGHT - 150)
        self.level_complete = False
        self.game_over = False  # Сбрасываем флаг проигрыша

    def run(self):
        running = True
        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Управление на WASD
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.player.jump()
                    if event.key == pygame.K_a:
                        self.player.velocity_x = -self.player.speed
                    if event.key == pygame.K_d:
                        self.player.velocity_x = self.player.speed
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a and self.player.velocity_x < 0:
                        self.player.velocity_x = 0
                    if event.key == pygame.K_d and self.player.velocity_x > 0:
                        self.player.velocity_x = 0

            if not self.paused and not self.level_complete and not self.game_over:
                # Обновление
                self.all_sprites.update()

                for platform in self.platforms:
                    if self.player.rect.colliderect(platform.rect):
                        if self.player.velocity_y > 0:  # Если игрок падает
                            self.player.rect.bottom = platform.rect.top
                            self.player.on_ground = True
                            self.player.velocity_y = 0
                        elif self.player.velocity_y < 0:  # Если игрок движется вверх
                            self.player.rect.top = platform.rect.bottom
                            self.player.velocity_y = 0
                        # Если игрок стоит на платформе
                        elif self.player.velocity_y == 0 and self.player.rect.bottom == platform.rect.top:
                            self.player.on_ground = True

                # Проверка завершения уровня
                if self.player.rect.colliderect(self.door.rect):
                    self.level_complete = True
                    if self.current_level < len(self.levels) - 1:
                        self.current_level += 1
                        self.load_level(self.current_level)
                    else:
                        self.show_victory_screen()

                # Проверка проигрыша (игрок упал за экран)
                if self.player.rect.bottom >= HEIGHT - 10:
                    self.game_over = True
                    self.show_game_over_screen()

            # Отрисовка
            screen.fill(BLACK)
            self.all_sprites.draw(screen)

            if self.level_complete:
                text = font.render("Уровень пройден!", True, GREEN)
                screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2))

            if self.paused:
                self.draw_pause_menu()

            if self.game_over:
                self.show_game_over_screen()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def show_game_over_screen(self):
        game_over_menu = True
        retry_button = Button("Попробовать снова", WIDTH // 2, HEIGHT // 2 - 50, GRAY, WHITE)
        main_menu_button = Button("В главное меню", WIDTH // 2, HEIGHT // 2 + 50, GRAY, WHITE)

        while game_over_menu:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_button.is_clicked(mouse_pos):
                        game_over_menu = False
                        self.load_level(self.current_level)  # Перезагружаем текущий уровень
                    if main_menu_button.is_clicked(mouse_pos):
                        game_over_menu = False
                        self.show_main_menu()

            screen.fill(BLACK)
            mouse_pos = pygame.mouse.get_pos()

            game_over_text = font.render("Игра окончена!", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 150))

            retry_button.check_hover(mouse_pos)
            main_menu_button.check_hover(mouse_pos)

            retry_button.draw(screen)
            main_menu_button.draw(screen)

            pygame.display.flip()

    def show_victory_screen(self):
        victory_menu = True
        main_menu_button = Button("В главное меню", WIDTH // 2, HEIGHT // 2 - 50, GRAY, WHITE)

        while victory_menu:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if main_menu_button.is_clicked(mouse_pos):
                        victory_menu = False
                        self.show_main_menu()

            screen.fill(BLACK)
            mouse_pos = pygame.mouse.get_pos()

            victory_text = font.render("Победа!", True, GREEN)
            screen.blit(victory_text, (WIDTH // 2 - 100, HEIGHT // 2 - 150))

            main_menu_button.check_hover(mouse_pos)
            main_menu_button.draw(screen)

            pygame.display.flip()

    def draw_pause_menu(self):
        pause_text = font.render("Пауза", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - 100, HEIGHT // 2 - 150))

        continue_button = Button("Продолжить", WIDTH // 2, HEIGHT // 2 - 50, GRAY, WHITE)
        main_menu_button = Button("В главное меню", WIDTH // 2, HEIGHT // 2 + 50, GRAY, WHITE)

        mouse_pos = pygame.mouse.get_pos()
        continue_button.check_hover(mouse_pos)
        main_menu_button.check_hover(mouse_pos)

        continue_button.draw(screen)
        main_menu_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.is_clicked(mouse_pos):
                    self.paused = False
                if main_menu_button.is_clicked(mouse_pos):
                    self.show_main_menu()

    def show_end_game_menu(self):
        end_game_menu = True
        main_menu_button = Button("В главное меню", WIDTH // 2, HEIGHT // 2 - 50, GRAY, WHITE)
        next_level_button = Button("Следующий уровень", WIDTH // 2, HEIGHT // 2 + 50, GRAY, WHITE)
        settings_button = Button("Настройки", WIDTH // 2, HEIGHT // 2 + 150, GRAY, WHITE)

        while end_game_menu:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if main_menu_button.is_clicked(mouse_pos):
                        end_game_menu = False
                        self.show_main_menu()
                    if next_level_button.is_clicked(mouse_pos):
                        end_game_menu = False
                        if self.current_level < len(self.levels) - 1:
                            self.current_level += 1
                            self.load_level(self.current_level)
                        else:
                            print("Это последний уровень!")
                    if settings_button.is_clicked(mouse_pos):
                        self.show_settings()

            screen.fill(BLACK)
            mouse_pos = pygame.mouse.get_pos()

            main_menu_button.check_hover(mouse_pos)
            next_level_button.check_hover(mouse_pos)
            settings_button.check_hover(mouse_pos)

            main_menu_button.draw(screen)
            next_level_button.draw(screen)
            settings_button.draw(screen)

            pygame.display.flip()

    def show_settings(self):
        settings_menu = True
        back_button = Button("Назад", WIDTH // 2, HEIGHT // 2 + 100, GRAY, WHITE)
        sound_button = Button("Звук: Вкл" if self.sound_enabled else "Звук: Выкл", WIDTH // 2, HEIGHT // 2 - 50, GRAY, WHITE)
        volume_up_button = Button("Громкость +", WIDTH // 2, HEIGHT // 2, GRAY, WHITE)
        volume_down_button = Button("Громкость -", WIDTH // 2, HEIGHT // 2 + 50, GRAY, WHITE)

        while settings_menu:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_clicked(mouse_pos):
                        settings_menu = False
                    if sound_button.is_clicked(mouse_pos):
                        self.sound_enabled = not self.sound_enabled
                        sound_button.text = "Звук: Вкл" if self.sound_enabled else "Звук: Выкл"
                    if volume_up_button.is_clicked(mouse_pos):
                        self.volume = min(1.0, self.volume + 0.1)
                    if volume_down_button.is_clicked(mouse_pos):
                        self.volume = max(0.0, self.volume - 0.1)

            screen.fill(BLACK)
            mouse_pos = pygame.mouse.get_pos()

            back_button.check_hover(mouse_pos)
            sound_button.check_hover(mouse_pos)
            volume_up_button.check_hover(mouse_pos)
            volume_down_button.check_hover(mouse_pos)

            back_button.draw(screen)
            sound_button.draw(screen)
            volume_up_button.draw(screen)
            volume_down_button.draw(screen)

            pygame.display.flip()

    def show_help(self):
        help_menu = True
        back_button = Button("Назад", WIDTH // 2, HEIGHT // 2 + 100, GRAY, WHITE)

        while help_menu:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_clicked(mouse_pos):
                        help_menu = False

            screen.fill(BLACK)
            mouse_pos = pygame.mouse.get_pos()

            help_text = small_font.render("Управление: WASD, Прыжок: W", True, WHITE)
            screen.blit(help_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

            back_button.check_hover(mouse_pos)
            back_button.draw(screen)

            pygame.display.flip()

    def show_level_select(self):
        level_select_menu = True
        back_button = Button("Назад", WIDTH // 2, HEIGHT // 2 + 100, GRAY, WHITE)
        level1_button = Button("Уровень 1", WIDTH // 2, HEIGHT // 2 - 50, GRAY, WHITE)
        level2_button = Button("Уровень 2", WIDTH // 2, HEIGHT // 2 + 50, GRAY, WHITE)

        while level_select_menu:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if level1_button.is_clicked(mouse_pos):
                        level_select_menu = False
                        self.current_level = 0
                        self.load_level(self.current_level)
                        self.run()
                    if level2_button.is_clicked(mouse_pos):
                        level_select_menu = False
                        self.current_level = 1
                        self.load_level(self.current_level)
                        self.run()
                    if back_button.is_clicked(mouse_pos):
                        level_select_menu = False

            screen.fill(BLACK)
            mouse_pos = pygame.mouse.get_pos()

            level1_button.check_hover(mouse_pos)
            level2_button.check_hover(mouse_pos)
            back_button.check_hover(mouse_pos)

            level1_button.draw(screen)
            level2_button.draw(screen)
            back_button.draw(screen)

            pygame.display.flip()

    def show_main_menu(self):
        main_menu = True
        play_button = Button("Играть", WIDTH // 2, HEIGHT // 2 - 150, GRAY, WHITE)
        settings_button = Button("Настройки", WIDTH // 2, HEIGHT // 2 - 50, GRAY, WHITE)
        help_button = Button("Помощь", WIDTH // 2, HEIGHT // 2 + 50, GRAY, WHITE)
        level_select_button = Button("Выбор уровня", WIDTH // 2, HEIGHT // 2 + 150, GRAY, WHITE)

        while main_menu:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.is_clicked(mouse_pos):
                        main_menu = False
                        self.current_level = 0
                        self.load_level(self.current_level)
                        self.run()
                    if settings_button.is_clicked(mouse_pos):
                        self.show_settings()
                    if help_button.is_clicked(mouse_pos):
                        self.show_help()
                    if level_select_button.is_clicked(mouse_pos):
                        self.show_level_select()

            screen.fill(BLACK)
            mouse_pos = pygame.mouse.get_pos()

            play_button.check_hover(mouse_pos)
            settings_button.check_hover(mouse_pos)
            help_button.check_hover(mouse_pos)
            level_select_button.check_hover(mouse_pos)

            play_button.draw(screen)
            settings_button.draw(screen)
            help_button.draw(screen)
            level_select_button.draw(screen)

            pygame.display.flip()