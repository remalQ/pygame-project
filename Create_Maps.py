import pickle
import os
import sys
from TextBox import *
import pygame

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
    6: {'name': 'move_on_approach', 'color': pygame.Color('skyblue'), 'solid': True},
    7: {'name': 'bouncing', 'color': pygame.Color('orange'), 'solid': True}  # Новый тип тайла
}

# Предустановленные цвета для текста (используются только в редакторе)
TEXT_COLORS = [
    (255, 255, 255),  # Белый
    (255, 0, 0),      # Красный
    (0, 255, 0),      # Зелёный
    (0, 0, 255),      # Синий
]

class LevelEditor:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Level Editor')
        self.clock = pygame.time.Clock()

        # Карта
        self.map_width = SCREEN_WIDTH // TILE_SIZE
        self.map_height = SCREEN_HEIGHT // TILE_SIZE
        self.grid = [[0 for _ in range(self.map_width)] for _ in range(self.map_height)]
        self.texts = []  # Список текстовых надписей

        # Состояние редактора
        self.current_tile = 1
        self.show_grid = True
        self.filename = ""
        self.mode = 'tiles'  # Режим: 'tiles' или 'text'
        self.selected_text = None  # Выбранный текст для редактирования
        self.dragging = False  # Флаг перетаскивания текста
        self.resizing = False  # Флаг изменения размера текста
        self.current_color_index = 0  # Индекс текущего цвета текста
        self.resize_start_pos = None  # Начальная позиция мыши при изменении размера
        self.resize_start_font_size = None  # Начальный размер шрифта при изменении размера

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

        if self.filename:  # Имя уже есть — просто сохранить
            self.save_level()
            return
        else:
            save_active = True

        while save_active:
            self.screen.fill(pygame.Color('black'))
            text = font.render("Введите имя уровня и нажмите Enter:", True, pygame.Color('white'))
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 70))
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
                        error_text = font.render("Имя не может быть пустым!", True, pygame.Color('red'))
                        self.screen.blit(error_text,
                                         (SCREEN_WIDTH // 2 - error_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
                        pygame.display.flip()
                        pygame.time.delay(1000)
            input_box.draw(self.screen)
            pygame.display.flip()

    def add_text_dialog(self, x, y):
        """Диалог для добавления нового текста"""
        input_box = TextInputBox(
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT // 2 - 25,
            300,
            50,
            font_size=30
        )
        font = pygame.font.SysFont('Arial', 30)
        active = True

        while active:
            self.screen.fill(pygame.Color('black'))
            prompt = font.render("Введите текст и нажмите Enter:", True, pygame.Color('white'))
            self.screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, SCREEN_HEIGHT // 2 - 70))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if input_box.handle_event(event):
                    if input_box.text:
                        self.texts.append({
                            'text': input_box.text,
                            'x': x,
                            'y': y,
                            'font_size': 30,
                            'color': TEXT_COLORS[self.current_color_index]
                        })
                        self.modified = True
                        active = False
            input_box.draw(self.screen)
            pygame.display.flip()

    def edit_text_dialog(self, text_obj):
        """Диалог для редактирования существующего текста"""
        input_box = TextInputBox(
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT // 2 - 25,
            300,
            50,
            font_size=30,
            initial_text=text_obj['text']
        )
        font = pygame.font.SysFont('Arial', 30)
        active = True

        while active:
            self.screen.fill(pygame.Color('black'))
            prompt = font.render("Введите новый текст и нажмите Enter:", True, pygame.Color('white'))
            self.screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, SCREEN_HEIGHT // 2 - 70))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if input_box.handle_event(event):
                    if input_box.text:
                        text_obj['text'] = input_box.text
                        self.modified = True
                        active = False
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
                        self.texts = []
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
                data = pickle.load(f)
                if isinstance(data, list):
                    # Старый формат: данные — это только двумерный список (grid)
                    self.grid = data
                    self.texts = []
                elif isinstance(data, dict):
                    # Новый формат: данные — словарь с grid и texts
                    self.grid = data.get('grid', [[0 for _ in range(self.map_width)] for _ in range(self.map_height)])
                    self.texts = data.get('texts', [])
                else:
                    raise ValueError("Неподдерживаемый формат данных уровня")
        except Exception as e:
            print(f"Ошибка загрузки уровня: {e}")
            self.grid = [[0 for _ in range(self.map_width)] for _ in range(self.map_height)]
            self.texts = []
        self.modified = False

    def save_level(self):
        """Сохранение уровня"""
        try:
            path = os.path.join(self.levels_dir, f"{self.filename}.pkl")
            data = {
                'grid': self.grid,
                'texts': self.texts
            }
            with open(path, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"Ошибка сохранения уровня: {e}")
        self.modified = False

    def get_resize_handle(self, text_obj, mouse_pos):
        """Проверяет, находится ли курсор мыши над уголком рамки текста"""
        font = pygame.font.Font("Fonts/Monocraft.otf", text_obj['font_size'])
        text_surf = font.render(text_obj['text'], True, text_obj['color'])
        text_rect = text_surf.get_rect(topleft=(text_obj['x'], text_obj['y']))
        # Определяем правый нижний уголок (10x10 пикселей)
        handle_rect = pygame.Rect(
            text_rect.right - 5, text_rect.bottom - 5, 10, 10
        )
        return handle_rect.collidepoint(mouse_pos)

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
                elif event.key == pygame.K_t:
                    self.mode = 'text' if self.mode == 'tiles' else 'tiles'
                    self.selected_text = None
                    self.resizing = False
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7):
                    if self.mode == 'tiles':
                        self.current_tile = event.key - pygame.K_0
                elif event.key == pygame.K_c and self.mode == 'text':
                    self.current_color_index = (self.current_color_index + 1) % len(TEXT_COLORS)
                elif event.key == pygame.K_DELETE and self.selected_text:
                    self.texts.remove(self.selected_text)
                    self.selected_text = None
                    self.modified = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.mode == 'tiles':
                    if event.button == 1 or event.button == 3:
                        self.selecting = True
                        self.start_select = (tile_x, tile_y)
                        self.end_select = (tile_x, tile_y)
                else:  # Режим текста
                    if event.button == 1:
                        # Проверяем, кликнули ли на уголок для изменения размера
                        if self.selected_text and self.get_resize_handle(self.selected_text, mouse_pos):
                            self.resizing = True
                            self.resize_start_pos = mouse_pos
                            self.resize_start_font_size = self.selected_text['font_size']
                        else:
                            # Проверяем, кликнули ли на существующий текст
                            for text_obj in self.texts:
                                font = pygame.font.Font("Fonts/Monocraft.otf", text_obj['font_size'])
                                text_surf = font.render(text_obj['text'], True, text_obj['color'])
                                text_rect = text_surf.get_rect(topleft=(text_obj['x'], text_obj['y']))
                                if text_rect.collidepoint(mouse_pos):
                                    self.selected_text = text_obj
                                    self.dragging = True
                                    break
                            else:
                                # Если не кликнули на текст, добавляем новый
                                self.selected_text = None
                                self.add_text_dialog(mouse_pos[0], mouse_pos[1])
                    elif event.button == 3 and self.selected_text:
                        self.edit_text_dialog(self.selected_text)

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.mode == 'tiles' and self.selecting:
                    self.fill_selection(event.button == 1)
                    self.selecting = False
                    self.start_select = None
                    self.end_select = None
                elif self.mode == 'text':
                    self.dragging = False
                    self.resizing = False
                    self.resize_start_pos = None
                    self.resize_start_font_size = None

            elif event.type == pygame.MOUSEMOTION:
                if self.mode == 'tiles' and self.selecting:
                    self.end_select = (tile_x, tile_y)
                elif self.mode == 'text':
                    if self.dragging and self.selected_text:
                        self.selected_text['x'] = mouse_pos[0]
                        self.selected_text['y'] = mouse_pos[1]
                        self.modified = True
                    elif self.resizing and self.selected_text:
                        # Изменение размера шрифта на основе перемещения мыши
                        dx = mouse_pos[0] - self.resize_start_pos[0]
                        dy = mouse_pos[1] - self.resize_start_pos[1]
                        # Используем среднее перемещение для масштабирования
                        delta = (dx + dy) / 2
                        new_font_size = self.resize_start_font_size + int(delta / 5)  # Чувствительность масштабирования
                        new_font_size = max(10, min(100, new_font_size))  # Ограничение: 10–100 пикселей
                        self.selected_text['font_size'] = new_font_size
                        self.modified = True

        return True

    def fill_selection(self, place_tile):
        """Заполняет выделенную область"""
        if self.start_select and self.end_select:
            x1, y1 = self.start_select
            x2, y2 = self.end_select
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y2, y1)
            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    if self.grid[y][x] != (self.current_tile if place_tile else 0):
                        self.grid[y][x] = self.current_tile if place_tile else 0
                        self.modified = True

    def draw_ui(self):
        """Отображение UI-информации"""
        font = pygame.font.SysFont('Arial', 20)
        mode_text = f"Режим: {'Тайлы' if self.mode == 'tiles' else 'Текст'} (T для смены)"
        mode_rendered = font.render(mode_text, True, pygame.Color('white'))
        self.screen.blit(mode_rendered, (10, 10))

        if self.mode == 'tiles':
            tile_name = TILE_TYPES[self.current_tile]['name']
            tool_text = f"Текущий: {tile_name} (1-7 для смены)"  # Обновлено для поддержки нового типа
        else:
            tool_text = f"Цвет: {self.current_color_index} (C для смены) | ЛКМ на угол: Масштаб | Del: Удалить"
        tool_rendered = font.render(tool_text, True, pygame.Color('white'))
        self.screen.blit(tool_rendered, (10, 30))

        help_text = "Ctrl+S: Сохранить | G: Сетка | ЛКМ: Добавить/Перетащить | ПКМ: Редактировать"
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

        # Отрисовка текстов
        for text_obj in self.texts:
            font = pygame.font.Font("Fonts/Monocraft.otf", text_obj['font_size'])
            text_surf = font.render(text_obj['text'], True, text_obj['color'])
            self.screen.blit(text_surf, (text_obj['x'], text_obj['y']))
            if text_obj == self.selected_text:
                text_rect = text_surf.get_rect(topleft=(text_obj['x'], text_obj['y']))
                pygame.draw.rect(self.screen, pygame.Color('white'), text_rect, 2)
                # Отрисовка маркера для правого нижнего уголка
                handle_rect = pygame.Rect(
                    text_rect.right - 5, text_rect.bottom - 5, 10, 10
                )
                pygame.draw.rect(self.screen, pygame.Color('red'), handle_rect)

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