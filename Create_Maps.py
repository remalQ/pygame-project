import pickle
import os
import sys
from TextBox import *

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
TILE_SIZE = 25
FPS = 60

# Типы тайлов
TILE_TYPES = {
    0: {'name': 'empty', 'color': pygame.Color('black'), 'solid': False},
    1: {'name': 'platform', 'color': pygame.Color('gray'), 'solid': True},
    2: {'name': 'door', 'color': pygame.Color('blue'), 'solid': False},
    3: {'name': 'coin', 'color': pygame.Color('yellow'), 'solid': False},
    4: {'name': 'breakable', 'color': pygame.Color('darkred'), 'solid': True},
    5: {'name': 'hover', 'color': pygame.Color('lightgreen'), 'solid': True},
    6: {'name': 'move_on_approach', 'color': pygame.Color('skyblue'), 'solid': True}

}


class LevelEditor:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Level Editor')
        self.clock = pygame.time.Clock()

        # Карта
        self.map_width = SCREEN_WIDTH // TILE_SIZE
        self.map_height = SCREEN_HEIGHT // TILE_SIZE
        self.grid = [[0 for _ in range(self.map_width)] for _ in range(self.map_height)]

        # Состояние редактора
        self.current_tile = 1
        self.show_grid = True
        self.filename = ""

        # Выделение
        self.selecting = False
        self.start_select = None
        self.end_select = None
        self.modified = False

        # Папка с уровнями
        self.levels_dir = "Maps"
        if not os.path.exists(self.levels_dir):
            os.makedirs(self.levels_dir)

        # Выбор уровня перед запуском редактора
        self.select_level_menu()

    def show_save_dialog(self):
        """Показывает диалог сохранения с вводом имени файла"""

        save_active = False
        input_box = TextInputBox(
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT // 2 - 25,
            300,
            50
        )
        font = pygame.font.SysFont('Arial', 30)

        if self.filename:  # имя уже есть — просто сохранить
            self.save_level()
            return

        else:
            save_active = True

        while save_active:
            self.screen.fill(pygame.Color('black'))

            # Рисуем текст инструкции
            text = font.render("Введите имя уровня и нажмите Enter:", True, pygame.Color('white'))
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 70))

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if input_box.handle_event(event):
                    if input_box.text:
                        self.filename = input_box.text
                        self.save_level()
                        save_active = False
                    else:
                        # Показываем сообщение об ошибке, если имя не введено
                        error_text = font.render("Имя не может быть пустым!", True, pygame.Color('red'))
                        self.screen.blit(error_text,
                                         (SCREEN_WIDTH // 2 - error_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
                        pygame.display.flip()
                        pygame.time.delay(1000)  # Задержка для отображения сообщения

            # Рисуем поле ввода
            input_box.draw(self.screen)
            pygame.display.flip()

    def select_level_menu(self):
        """Меню выбора уровня перед запуском редактора"""
        running = True
        font = pygame.font.SysFont('Arial', 30)

        while running:
            self.screen.fill(pygame.Color('black'))
            title = font.render("Выберите уровень для редактирования", True, pygame.Color('white'))
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

            levels = [f[:-4] for f in os.listdir(self.levels_dir) if f.endswith('.pkl')]
            levels.append("Создать новый уровень")

            mouse_pos = pygame.mouse.get_pos()
            y_offset = 150
            selected = None

            for index, level_name in enumerate(levels):
                level_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, y_offset, 300, 50)
                color = pygame.Color('gray') if level_rect.collidepoint(mouse_pos) else pygame.Color('white')

                pygame.draw.rect(self.screen, color, level_rect)
                text = font.render(level_name, True, pygame.Color('black'))
                self.screen.blit(text, (level_rect.x + 10, level_rect.y + 10))

                if level_rect.collidepoint(mouse_pos):
                    selected = level_name

                y_offset += 60

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and selected:
                    if selected == "Создать новый уровень":
                        self.filename = self.get_new_level_name()
                        self.grid = [[0 for _ in range(self.map_width)] for _ in range(self.map_height)]
                    else:
                        self.filename = selected
                        self.load_level()
                    running = False

            pygame.display.flip()

    def get_new_level_name(self):
        """Генерация имени нового уровня"""
        existing_levels = {f[:-4] for f in os.listdir(self.levels_dir) if f.endswith('.pkl')}
        num = 1
        while f"level{num}" in existing_levels:
            num += 1
        return f"level{num}"

    def load_level(self):
        """Загрузка уровня из файла"""
        try:
            path = os.path.join(self.levels_dir, f"{self.filename}.pkl")
            with open(path, 'rb') as f:
                self.grid = pickle.load(f)
        except Exception:
            pass
        self.modified = False  # загрузили — изменений нет

    def save_level(self):
        """Сохранение уровня"""
        try:
            path = os.path.join(self.levels_dir, f"{self.filename}.pkl")
            with open(path, 'wb') as f:
                pickle.dump(self.grid, f)
        except Exception:
            pass
        self.modified = False  # после сохранения — изменений нет

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        tile_x, tile_y = mouse_pos[0] // TILE_SIZE, mouse_pos[1] // TILE_SIZE

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.modified:
                        if self.ask_save_confirmation():
                            self.save_level()
                    self.select_level_menu()

                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.show_save_dialog()
                elif event.key == pygame.K_g:
                    self.show_grid = not self.show_grid
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6):
                    self.current_tile = event.key - pygame.K_0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 or event.button == 3:  # ЛКМ или ПКМ
                    self.selecting = True
                    self.start_select = (tile_x, tile_y)
                    self.end_select = (tile_x, tile_y)

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.selecting:
                    self.fill_selection(event.button == 1)  # ЛКМ - заполнить, ПКМ - удалить
                    self.selecting = False
                    self.start_select = None
                    self.end_select = None

            elif event.type == pygame.MOUSEMOTION:
                if self.selecting:
                    self.end_select = (tile_x, tile_y)

        return True

    def fill_selection(self, place_tile):
        """Заполняет выделенную область"""
        if self.start_select and self.end_select:
            x1, y1 = self.start_select
            x2, y2 = self.end_select
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)

            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    if self.grid[y][x] != (self.current_tile if place_tile else 0):
                        self.grid[y][x] = self.current_tile if place_tile else 0
                        self.modified = True

    def draw_ui(self):
        """Отображение UI-информации"""
        font = pygame.font.SysFont('Arial', 20)

        # Название текущего тайла
        tile_name = TILE_TYPES[self.current_tile]['name']
        tool_text = font.render(f"Текущий: {tile_name} (1-6 для смены)", True, pygame.Color('white'))

        self.screen.blit(tool_text, (10, 10))

        # Подсказки по управлению
        help_text = "Ctrl+S: Сохранить | G: Сетка | ЛКМ: Залить | ПКМ: Удалить"
        help_rendered = font.render(help_text, True, pygame.Color('white'))
        self.screen.blit(help_rendered, (10, SCREEN_HEIGHT - 30))

    def draw(self):
        self.screen.fill(pygame.Color('black'))

        for y in range(self.map_height):
            for x in range(self.map_width):
                tile_type = self.grid[y][x]
                color = TILE_TYPES[tile_type]['color']
                pygame.draw.rect(self.screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        if self.show_grid:
            for y in range(self.map_height):
                for x in range(self.map_width):
                    pygame.draw.rect(self.screen, pygame.Color('darkgray'),
                                     (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

        if self.selecting and self.start_select and self.end_select:
            x1, y1 = self.start_select
            x2, y2 = self.end_select
            pygame.draw.rect(self.screen, pygame.Color('white'),
                             (x1 * TILE_SIZE, y1 * TILE_SIZE, (x2 - x1 + 1) * TILE_SIZE, (y2 - y1 + 1) * TILE_SIZE), 2)

        self.draw_ui()
        pygame.display.flip()

    def ask_save_confirmation(self):
        """Диалог подтверждения сохранения"""
        font = pygame.font.SysFont('Arial', 30)
        yes_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 30, 100, 50)
        no_rect = pygame.Rect(SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 30, 100, 50)

        while True:
            self.screen.fill(pygame.Color('black'))
            prompt = font.render("Сохранить изменения?", True, pygame.Color('white'))
            self.screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

            pygame.draw.rect(self.screen, pygame.Color('green'), yes_rect)
            pygame.draw.rect(self.screen, pygame.Color('red'), no_rect)

            yes_text = font.render("Да", True, pygame.Color('black'))
            no_text = font.render("Нет", True, pygame.Color('black'))
            self.screen.blit(yes_text, (yes_rect.x + 25, yes_rect.y + 10))
            self.screen.blit(no_text, (no_rect.x + 25, no_rect.y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_rect.collidepoint(event.pos):
                        return True
                    elif no_rect.collidepoint(event.pos):
                        return False

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    editor = LevelEditor()
    editor.run()