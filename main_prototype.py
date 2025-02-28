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
        self.velocity_y += 0.5
        self.rect.y += self.velocity_y

        # Движение по горизонтали
        self.rect.x += self.velocity_x

        # Ограничение выхода за пределы экрана по горизонтали
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        # Ограничение падения
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.on_ground = True
            self.velocity_y = 0

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
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.hover_color if self.hovered else self.color, self.rect)
        text_surface = small_font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.hovered


# Основной класс игры
class Game:
    def __init__(self):
        self.player = Player()
        self.platforms = pygame.sprite.Group()
        self.door = Door(WIDTH - 100, HEIGHT - 150)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player, self.door)

        # Создание платформ
        self.platforms.add(Platform(0, HEIGHT - 50, WIDTH, 50))  # Пол
        self.platforms.add(Platform(200, 400, 100, 20))         # Платформа 1
        self.platforms.add(Platform(500, 300, 100, 20))         # Платформа 2
        self.all_sprites.add(self.platforms)

        self.level_complete = False
        self.paused = False
        self.sound_enabled = True
        self.volume = 0.5

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

            if not self.paused and not self.level_complete:
                # Обновление
                self.all_sprites.update()

                # Проверка коллизий с платформами
                for platform in self.platforms:
                    if self.player.rect.colliderect(platform.rect):
                        if self.player.velocity_y > 0:  # Если игрок падает
                            self.player.rect.bottom = platform.rect.top
                            self.player.on_ground = True
                            self.player.velocity_y = 0
                        elif self.player.velocity_y < 0:  # Если игрок движется вверх
                            self.player.rect.top = platform.rect.bottom
                            self.player.velocity_y = 0

                # Проверка завершения уровня
                if self.player.rect.colliderect(self.door.rect):
                    self.level_complete = True

            # Отрисовка
            screen.fill(BLACK)
            self.all_sprites.draw(screen)

            if self.level_complete:
                text = font.render("Уровень пройден!", True, GREEN)
                screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2))

            if self.paused:
                self.draw_pause_menu()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def draw_pause_menu(self):
        pause_text = font.render("Пауза", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - 100, HEIGHT // 2 - 150))

        continue_button = Button("Продолжить", WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, GRAY, WHITE)
        main_menu_button = Button("В главное меню", WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, GRAY, WHITE)

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

    def show_main_menu(self):
        main_menu = True
        play_button = Button("Играть", WIDTH // 2 - 100, HEIGHT // 2 - 150, 200, 50, GRAY, WHITE)
        settings_button = Button("Настройки", WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, GRAY, WHITE)
        help_button = Button("Помощь", WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, GRAY, WHITE)
        level_select_button = Button("Выбор уровня", WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50, GRAY, WHITE)

        while main_menu:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

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

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.is_clicked(mouse_pos):
                        main_menu = False
                        self.run()
                    if settings_button.is_clicked(mouse_pos):
                        self.show_settings()
                    if help_button.is_clicked(mouse_pos):
                        self.show_help()
                    if level_select_button.is_clicked(mouse_pos):
                        self.show_level_select()

            pygame.display.flip()

    def show_settings(self):
        settings_menu = True
        back_button = Button("Назад", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, GRAY, WHITE)
        sound_button = Button("Звук: Вкл" if self.sound_enabled else "Звук: Выкл", WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, GRAY, WHITE)
        volume_up_button = Button("Громкость +", WIDTH // 2 - 100, HEIGHT // 2, 200, 50, GRAY, WHITE)
        volume_down_button = Button("Громкость -", WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, GRAY, WHITE)

        while settings_menu:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

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

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_clicked(mouse_pos):
                        settings_menu = False
                    if sound_button.is_clicked(mouse_pos):
                        self.sound_enabled = not self.sound_enabled
                        sound_button.text = "Звук: Вкл" if self.sound_enabled else "Звук: Выкл"
                    if volume_up_button.is_clicked(mouse_pos):
                        self.volume = min(1.0, self.volume + 0.1)
                    if volume_down_button.is_clicked(mouse_pos):
                        self.volume = max(0.0, self.volume - 0.1)

            pygame.display.flip()

    def show_help(self):
        help_menu = True
        back_button = Button("Назад", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, GRAY, WHITE)

        while help_menu:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(BLACK)
            mouse_pos = pygame.mouse.get_pos()

            help_text = small_font.render("Управление: WASD, Прыжок: W", True, WHITE)
            screen.blit(help_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

            back_button.check_hover(mouse_pos)
            back_button.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_clicked(mouse_pos):
                        help_menu = False

            pygame.display.flip()

    def show_level_select(self):
        level_select_menu = True
        back_button = Button("Назад", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, GRAY, WHITE)
        level1_button = Button("Уровень 1", WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, GRAY, WHITE)

        while level_select_menu:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(BLACK)
            mouse_pos = pygame.mouse.get_pos()

            level1_button.check_hover(mouse_pos)
            back_button.check_hover(mouse_pos)

            level1_button.draw(screen)
            back_button.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if level1_button.is_clicked(mouse_pos):
                        level_select_menu = False
                        self.run()
                    if back_button.is_clicked(mouse_pos):
                        level_select_menu = False

            pygame.display.flip()


# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.show_main_menu()
