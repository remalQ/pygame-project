import os
import sys
import pickle
import pygame
from TextBox import TextInputBox

pygame.init()

SCREEN_WIDTH  = 1000
SCREEN_HEIGHT = 800
TILE_SIZE     = 25
FPS           = 60

# Типы тайлов
TILE_TYPES = {
    0: {'name': 'empty',           'color': pygame.Color('black'),      'solid': False},
    1: {'name': 'platform',        'color': pygame.Color('gray'),       'solid': True},
    2: {'name': 'door',            'color': pygame.Color('blue'),       'solid': False},
    3: {'name': 'coin',            'color': pygame.Color('yellow'),     'solid': False},
    4: {'name': 'breakable',       'color': pygame.Color('darkred'),    'solid': True},
    5: {'name': 'hover',           'color': pygame.Color('lightgreen'), 'solid': True},
    6: {'name': 'move_on_approach','color': pygame.Color('skyblue'),    'solid': True},
    7: {'name': 'bouncing',        'color': pygame.Color('orange'),     'solid': True},
    8: {'name': 'password_box',    'color': pygame.Color('cyan'),       'solid': False},
}

TEXT_COLORS = [
    (255, 255, 255),  # белый
    (255,   0,   0),  # красный
    (  0, 255,   0),  # зелёный
    (  0,   0, 255),  # синий
]

class LevelEditor:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Level Editor')
        self.clock = pygame.time.Clock()

        self.map_width  = SCREEN_WIDTH // TILE_SIZE
        self.map_height = SCREEN_HEIGHT // TILE_SIZE

        # Данные уровня
        self.grid  = [[0] * self.map_width for _ in range(self.map_height)]
        self.texts = []
        self.zones = []
        self.password_positions = []  # Список позиций боксов с паролем

        self.filename = ""

        self.mode = 'tiles'
        self.current_tile = 1
        self.current_color_index = 0

        self.show_grid = True
        self.selecting = False
        self.start_select = None
        self.end_select = None

        self.selected_text = None
        self.dragging = False
        self.resizing = False
        self.resize_start_pos = None
        self.resize_start_font_size = None

        self.drawing_zone = False
        self.zone_start = None

        self.modified = False

        self.levels_dir = "Maps"
        os.makedirs(self.levels_dir, exist_ok=True)

        self.select_level_menu()

    def select_level_menu(self):
        font = pygame.font.SysFont('Arial', 30)
        running = True
        while running:
            self.screen.fill(pygame.Color('black'))
            title = font.render("Выберите уровень для редактирования", True, pygame.Color('white'))
            self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))

            files = [f[:-4] for f in os.listdir(self.levels_dir) if f.endswith('.pkl')]
            files.append("Создать новый уровень")

            mouse = pygame.mouse.get_pos()
            y = 150
            selected = None
            for name in files:
                rect = pygame.Rect(SCREEN_WIDTH//2-150, y, 300, 50)
                color = pygame.Color('gray') if rect.collidepoint(mouse) else pygame.Color('white')
                pygame.draw.rect(self.screen, color, rect)
                label = font.render(name, True, pygame.Color('black'))
                self.screen.blit(label, (rect.x+10, rect.y+10))
                if rect.collidepoint(mouse):
                    selected = name
                y += 60

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN and selected:
                    if selected == "Создать новый уровень":
                        self.filename = ""
                        self.grid = [[0]*self.map_width for _ in range(self.map_height)]
                        self.texts = []
                        self.zones = []
                        self.password_positions = []
                    else:
                        self.filename = selected
                        self.load_level()
                    running = False

            pygame.display.flip()
            self.clock.tick(FPS)

    def load_level(self):
        path = os.path.join(self.levels_dir, f"{self.filename}.pkl")
        try:
            with open(path, 'rb') as f:
                data = pickle.load(f)
            self.grid  = data.get('grid', self.grid)
            self.texts = data.get('texts', [])
            self.zones = data.get('zones', [])
            self.password_positions = data.get('password_positions', [])
        except Exception as e:
            print(f"Ошибка загрузки уровня: {e}")
            self.grid  = [[0]*self.map_width for _ in range(self.map_height)]
            self.texts = []
            self.zones = []
            self.password_positions = []
        self.modified = False

    def save_level(self):
        if not self.filename:
            return self.show_save_dialog()

        path = os.path.join(self.levels_dir, f"{self.filename}.pkl")
        data = {
            'grid':  self.grid,
            'texts': self.texts,
            'zones': self.zones,
            'password_positions': self.password_positions,
        }
        try:
            with open(path, 'wb') as f:
                pickle.dump(data, f)
            self.modified = False
        except Exception as e:
            print(f"Ошибка сохранения уровня: {e}")

    def show_save_dialog(self):
        box = TextInputBox(SCREEN_WIDTH//2-150, SCREEN_HEIGHT//2-25, 300, 50)
        font = pygame.font.SysFont('Arial', 30)
        active = True
        while active:
            self.screen.fill(pygame.Color('black'))
            prompt = font.render("Введите имя уровня и нажмите Enter:", True, pygame.Color('white'))
            self.screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, SCREEN_HEIGHT//2 - 70))

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if box.handle_event(ev):
                    if box.text.strip():
                        self.filename = box.text.strip()
                        self.save_level()
                        active = False

            box.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

    def add_text_dialog(self, x, y):
        box = TextInputBox(SCREEN_WIDTH//2-150, SCREEN_HEIGHT//2-25, 300, 50, font_size=30)
        font = pygame.font.SysFont('Arial', 30)
        active = True
        while active:
            self.screen.fill(pygame.Color('black'))
            prompt = font.render("Введите текст и нажмите Enter:", True, pygame.Color('white'))
            self.screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, SCREEN_HEIGHT//2 - 70))

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if box.handle_event(ev):
                    if box.text.strip():
                        self.texts.append({
                            'text': box.text,
                            'x': x,
                            'y': y,
                            'font_size': 30,
                            'color': TEXT_COLORS[self.current_color_index]
                        })
                        self.modified = True
                        active = False

            box.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

    def edit_text_dialog(self, text_obj):
        box = TextInputBox(SCREEN_WIDTH//2-150, SCREEN_HEIGHT//2-25, 300, 50,
                           font_size=text_obj['font_size'],
                           initial_text=text_obj['text'])
        font = pygame.font.SysFont('Arial', 30)
        active = True
        while active:
            self.screen.fill(pygame.Color('black'))
            prompt = font.render("Редактируйте текст и нажмите Enter:", True, pygame.Color('white'))
            self.screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, SCREEN_HEIGHT//2 - 70))

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if box.handle_event(ev):
                    text_obj['text'] = box.text
                    self.modified = True
                    active = False

            box.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

    def ask_zone_effect(self):
        box = TextInputBox(SCREEN_WIDTH//2-150, SCREEN_HEIGHT//2-25, 300, 50)
        font = pygame.font.SysFont('Arial', 24)
        prompt = (
            "1: low_gravity (gravity x0.3)\n"
            "2: ghost_mode\n"
            "Введите 1–2 и нажмите Enter:"
        )
        choice = None
        while choice is None:
            self.screen.fill(pygame.Color('black'))
            for i, line in enumerate(prompt.split("\n")):
                self.screen.blit(font.render(line, True, pygame.Color('white')),
                                 (50, SCREEN_HEIGHT//2 - 80 + i*30))
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if box.handle_event(ev):
                    try:
                        n = int(box.text.strip())
                        if n in (1,2):
                            choice = n
                    except:
                        pass
            box.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

        if choice == 1:
            return 'low_gravity', 0.3
        else:
            return 'ghost_mode', 1.0

    def get_resize_handle(self, text_obj, mouse_pos):
        font = pygame.font.Font("Fonts/Monocraft.otf", text_obj['font_size'])
        surf = font.render(text_obj['text'], True, text_obj['color'])
        rect = surf.get_rect(topleft=(text_obj['x'], text_obj['y']))
        handle = pygame.Rect(rect.right - 5, rect.bottom - 5, 10, 10)
        return handle.collidepoint(mouse_pos)

    def fill_selection(self, place_tile):
        if not (self.start_select and self.end_select):
            return
        x1, y1 = self.start_select
        x2, y2 = self.end_select
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        for ty in range(y1, y2+1):
            for tx in range(x1, x2+1):
                new_val = self.current_tile if place_tile else 0
                # Специальная обработка для password_box (тип 8)
                if new_val == 8:
                    box_width = 4  # число тайлов по ширине
                    box_height = 4  # число тайлов по высоте
                    # Очищаем все клетки под боксом
                    for dy in range(box_height):
                        for dx in range(box_width):
                            if 0 <= ty + dy < self.map_height and 0 <= tx + dx < self.map_width:
                                self.grid[ty + dy][tx + dx] = 0
                    # Ставим тип 8 в верхний левый угол
                    self.grid[ty][tx] = 8
                    pos = {
                        'x': tx * TILE_SIZE,
                        'y': ty * TILE_SIZE,
                        'w': box_width * TILE_SIZE,
                        'h': box_height * TILE_SIZE
                    }
                    if pos not in self.password_positions:
                        self.password_positions.append(pos)
                    self.modified = True




                elif new_val == 0:

                    # Проверяем, есть ли здесь password_box
                    is_password_box = False
                    box_w, box_h = 1, 1
                    to_remove = None
                    for pos in self.password_positions:
                        x0 = pos['x'] // TILE_SIZE
                        y0 = pos['y'] // TILE_SIZE
                        w = pos.get('w', TILE_SIZE * 4) // TILE_SIZE
                        h = pos.get('h', TILE_SIZE * 4) // TILE_SIZE
                        # Если (tx, ty) попал в зону password_box

                        if x0 <= tx < x0 + w and y0 <= ty < y0 + h:
                            is_password_box = True
                            box_w, box_h = w, h
                            to_remove = pos
                            break

                    if is_password_box and to_remove:
                        # Удаляем password_box
                        for dy in range(box_h):
                            for dx in range(box_w):
                                if 0 <= (y0 + dy) < self.map_height and 0 <= (x0 + dx) < self.map_width:
                                    self.grid[y0 + dy][x0 + dx] = 0
                        self.password_positions.remove(to_remove)
                        self.modified = True

                    else:
                        # Просто обычная платформа — удаляем только 1 тайл
                        self.grid[ty][tx] = 0
                        self.modified = True



                else:
                    # Обычные тайлы
                    if self.grid[ty][tx] != new_val:
                        self.grid[ty][tx] = new_val
                        self.modified = True

    def handle_events(self):
        mouse = pygame.mouse.get_pos()
        mx, my = mouse
        tile_x, tile_y = mx // TILE_SIZE, my // TILE_SIZE
        keys = pygame.key.get_pressed()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return False

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    if self.modified:
                        if self.ask_save_confirmation():
                            self.save_level()
                    self.select_level_menu()
                elif ev.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    self.save_level()
                elif ev.key == pygame.K_g:
                    self.show_grid = not self.show_grid
                elif ev.key == pygame.K_t:
                    self.mode = 'text' if self.mode != 'text' else 'tiles'
                elif ev.key == pygame.K_z:
                    self.mode = 'zones' if self.mode != 'zones' else 'tiles'
                elif ev.key in (pygame.K_1, pygame.K_2, pygame.K_3,
                                pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8):
                    if self.mode == 'tiles':
                        self.current_tile = ev.key - pygame.K_0
                elif ev.key == pygame.K_c and self.mode == 'text':
                    self.current_color_index = (self.current_color_index + 1) % len(TEXT_COLORS)

            if self.mode == 'tiles':
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button in (1, 3):
                    self.selecting = True
                    self.start_select = (tile_x, tile_y)
                    self.end_select = (tile_x, tile_y)
                elif ev.type == pygame.MOUSEMOTION and self.selecting:
                    self.end_select = (tile_x, tile_y)
                elif ev.type == pygame.MOUSEBUTTONUP and ev.button in (1, 3) and self.selecting:
                    self.fill_selection(place_tile=(ev.button == 1))
                    self.selecting = False
                    self.start_select = None
                    self.end_select = None

            elif self.mode == 'text':
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if self.selected_text and self.get_resize_handle(self.selected_text, mouse):
                        self.resizing = True
                        self.resize_start_pos = mouse
                        self.resize_start_font_size = self.selected_text['font_size']
                    else:
                        for t in self.texts:
                            font = pygame.font.Font("Fonts/Monocraft.otf", t['font_size'])
                            surf = font.render(t['text'], True, t['color'])
                            rect = surf.get_rect(topleft=(t['x'], t['y']))
                            if rect.collidepoint(mouse):
                                self.selected_text = t
                                self.dragging = True
                                break
                        else:
                            self.selected_text = None
                            self.add_text_dialog(mx, my)
                elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 3 and self.selected_text:
                    self.edit_text_dialog(self.selected_text)
                elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                    self.dragging = False
                    self.resizing = False
                elif ev.type == pygame.MOUSEMOTION:
                    if self.dragging and self.selected_text:
                        self.selected_text['x'], self.selected_text['y'] = mouse
                        self.modified = True
                    elif self.resizing and self.selected_text:
                        dx = mouse[0] - self.resize_start_pos[0]
                        dy = mouse[1] - self.resize_start_pos[1]
                        delta = (dx + dy) / 2
                        new_size = self.resize_start_font_size + int(delta / 5)
                        new_size = max(10, min(100, new_size))
                        self.selected_text['font_size'] = new_size
                        self.modified = True
                elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_DELETE and self.selected_text:
                    self.texts.remove(self.selected_text)
                    self.selected_text = None
                    self.modified = True

            elif self.mode == 'zones':
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self.zone_start = (tile_x, tile_y)
                    self.drawing_zone = True
                elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1 and self.drawing_zone:
                    tx0, ty0 = self.zone_start
                    tx1, ty1 = tile_x, tile_y
                    x1, x2 = min(tx0, tx1), max(tx0, tx1)
                    y1, y2 = min(ty0, ty1), max(ty0, ty1)
                    rect = pygame.Rect(
                        x1 * TILE_SIZE,
                        y1 * TILE_SIZE,
                        (x2 - x1 + 1) * TILE_SIZE,
                        (y2 - y1 + 1) * TILE_SIZE
                    )
                    effect, value = self.ask_zone_effect()
                    self.zones.append({
                        'x': rect.x, 'y': rect.y,
                        'w': rect.w, 'h': rect.h,
                        'effect': effect, 'value': value
                    })
                    self.modified = True
                    self.drawing_zone = False
                    self.zone_start = None
                elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 3:
                    for zone in self.zones:
                        zr = pygame.Rect(zone['x'], zone['y'], zone['w'], zone['h'])
                        if zr.collidepoint(mx, my):
                            self.zones.remove(zone)
                            self.modified = True
                            break

        return True

    def draw_ui(self):
        font = pygame.font.SysFont('Arial', 20)
        mode_name = {
            'tiles': 'Тайлы',
            'text':  'Текст',
            'zones': 'Зоны'
        }[self.mode]
        mode_text = f"Режим: {mode_name} (T:Текст, Z:Зоны)"
        self.screen.blit(font.render(mode_text, True, pygame.Color('white')), (10, 10))

        if self.mode == 'tiles':
            tile_name = TILE_TYPES[self.current_tile]['name']
            tool_text = f"Текущий тайл: {tile_name} (1-8 смена)"
        else:
            tool_text = f"Цвет текста: {self.current_color_index} (C смена)" if self.mode=='text' \
                        else "Рисуйте зоны ЛКМ+Drag"
        self.screen.blit(font.render(tool_text, True, pygame.Color('white')), (10, 30))

        help_text = "Ctrl+S:Сохранить | G:Сетка | Esc:Меню"
        self.screen.blit(font.render(help_text, True, pygame.Color('white')), (10, SCREEN_HEIGHT-30))

    def draw(self):
        self.screen.fill(pygame.Color('black'))
        mx, my = pygame.mouse.get_pos()

        for y in range(self.map_height):
            for x in range(self.map_width):
                t = self.grid[y][x]
                color = TILE_TYPES[t]['color']
                pygame.draw.rect(self.screen, color,
                                 (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

        if self.show_grid:
            for y in range(self.map_height):
                for x in range(self.map_width):
                    pygame.draw.rect(self.screen, pygame.Color('darkgray'),
                                     (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

        if self.mode == 'tiles' and self.selecting and self.start_select and self.end_select:
            x1, y1 = self.start_select
            x2, y2 = self.end_select
            rect = pygame.Rect(x1*TILE_SIZE, y1*TILE_SIZE,
                               (x2-x1+1)*TILE_SIZE, (y2-y1+1)*TILE_SIZE)
            pygame.draw.rect(self.screen, pygame.Color('white'), rect, 2)

        for z in self.zones:
            s = pygame.Surface((z['w'], z['h']), pygame.SRCALPHA)
            s.fill((255, 165, 0, 80))
            self.screen.blit(s, (z['x'], z['y']))

        if self.mode == 'zones' and self.drawing_zone and self.zone_start:
            tx0, ty0 = self.zone_start
            tx1, ty1 = mx // TILE_SIZE, my // TILE_SIZE
            x1, x2 = min(tx0, tx1), max(tx0, tx1)
            y1, y2 = min(ty0, ty1), max(ty0, ty1)
            preview = pygame.Rect(
                x1 * TILE_SIZE,
                y1 * TILE_SIZE,
                (x2 - x1 + 1) * TILE_SIZE,
                (y2 - y1 + 1) * TILE_SIZE
            )
            pygame.draw.rect(self.screen, pygame.Color('orange'), preview, 2)

        for t in self.texts:
            font = pygame.font.Font("Fonts/Monocraft.otf", t['font_size'])
            surf = font.render(t['text'], True, t['color'])
            self.screen.blit(surf, (t['x'], t['y']))
            if t is self.selected_text and self.mode=='text':
                rect = surf.get_rect(topleft=(t['x'], t['y']))
                pygame.draw.rect(self.screen, pygame.Color('white'), rect, 2)
                handle = pygame.Rect(rect.right-5, rect.bottom-5, 10, 10)
                pygame.draw.rect(self.screen, pygame.Color('red'), handle)

        self.draw_ui()
        pygame.display.flip()

    def ask_save_confirmation(self):
        font = pygame.font.SysFont('Arial', 30)
        yes_rect = pygame.Rect(SCREEN_WIDTH//2-120, SCREEN_HEIGHT//2+30, 100, 50)
        no_rect  = pygame.Rect(SCREEN_WIDTH//2 +20, SCREEN_HEIGHT//2+30, 100, 50)

        while True:
            self.screen.fill(pygame.Color('black'))
            prompt = font.render("Сохранить изменения?", True, pygame.Color('white'))
            self.screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, SCREEN_HEIGHT//2 - 50))
            pygame.draw.rect(self.screen, pygame.Color('green'), yes_rect)
            pygame.draw.rect(self.screen, pygame.Color('red'),   no_rect)
            self.screen.blit(font.render("Да", True, pygame.Color('black')), (yes_rect.x+25, yes_rect.y+10))
            self.screen.blit(font.render("Нет", True, pygame.Color('black')), (no_rect.x+25,  no_rect.y+10))
            pygame.display.flip()

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if yes_rect.collidepoint(ev.pos):
                        return True
                    if no_rect.collidepoint(ev.pos):
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