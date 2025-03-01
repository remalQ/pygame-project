import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 1600, 900
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("I Hate This Game")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Шрифты
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, HEIGHT - 150)
        self.velocity_y = 0
        self.velocity_x = 0
        self.on_ground = False
        self.speed = 5

    def update(self):
        # Гравитация
        if not self.on_ground:
            self.velocity_y += 0.5

        # Движение по вертикали
        self.rect.y += self.velocity_y

        # Движение по горизонтали
        self.rect.x += self.velocity_x

        # Ограничение выхода за пределы экрана по горизонтали
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def jump(self):
        if self.on_ground:
            self.velocity_y = -12
            self.on_ground = False



# Класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


# Класс двери
class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 100))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


# Класс кнопки
class Button:
    def __init__(self, text, center_x, center_y, color, hover_color, padding_x=20, padding_y=10):
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.padding_x = padding_x  # Отступ по горизонтали
        self.padding_y = padding_y  # Отступ по вертикали

        # Создаём поверхность с текстом
        self.text_surface = small_font.render(self.text, True, BLACK)
        self.text_rect = self.text_surface.get_rect()

        # Рассчитываем размер кнопки на основе текста и отступов
        self.width = self.text_rect.width + 2 * self.padding_x
        self.height = self.text_rect.height + 2 * self.padding_y

        # Прямоугольник кнопки (центрируем)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (center_x, center_y)  # Центрируем кнопку
        self.hovered = False

    def draw(self, screen):
        # Отрисовка кнопки с учётом состояния hovered
        pygame.draw.rect(screen, self.hover_color if self.hovered else self.color, self.rect)
        # Центрируем текст внутри кнопки
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        self.check_hover(mouse_pos)
        return self.hovered


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
            self.create_level_1(),  # Уровень 1
            self.create_level_2(),  # Уровень 2
        ]
        self.current_level = 0
        self.load_level(self.current_level)

        self.level_complete = False
        self.paused = False
        self.game_over = False  # Флаг для отслеживания проигрыша
        self.sound_enabled = True
        self.volume = 0.5

    def create_level_1(self):
        # Уровень 1
        platforms = [
            Platform(0, HEIGHT - 50, WIDTH / 2 - 100, 50),  # Левая половина пола
            Platform(WIDTH / 2 + 100, HEIGHT - 50, WIDTH / 2 - 100, 50),  # Правая половина пола
            Platform(200, HEIGHT - 200, 100, 20),  # Платформа 1
            Platform(500, HEIGHT - 150, 100, 20),  # Платформа 2
        ]
        door = Door(WIDTH - 100, HEIGHT - 150)  # Дверь
        return platforms, door

    def create_level_2(self):
        # Уровень 2
        platforms = [
            Platform(0, HEIGHT - 50, WIDTH, 50),  # Пол
            Platform(300, 600, 200, 20),         # Платформа 1
            Platform(600, 400, 150, 20),         # Платформа 2
            Platform(1000, 200, 100, 20),        # Платформа 3
        ]
        door = Door(WIDTH - 100, 100)            # Дверь вверху
        return platforms, door

    def load_level(self, level_index):
        # Загружаем уровень
        self.platforms.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)

        platforms, door = self.levels[level_index]
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


# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.show_main_menu()
