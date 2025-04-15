import pygame
from Button import Button
from Const_Values import *


class LeaderboardMenu:
    def __init__(self, records_db):
        self.records_db = records_db
        self.level_buttons = []

        # Создаем кнопки с учетом нового стиля Button
        self.all_button = Button("Все уровни", WIDTH // 2, 150, GRAY, LIGHT_GRAY)
        self.back_button = Button("Назад", WIDTH // 2, HEIGHT - 100, GRAY, LIGHT_GRAY)

        # Создаем кнопки для каждого уровня (максимум 10 уровней)
        for i in range(1, 11):
            btn = Button(f"Ур. {i}", 100 + (i - 1) * 80, 200, GRAY, LIGHT_GRAY)
            btn.rect = pygame.Rect(100 + (i - 1) * 80 - 35, 175, 70, 40)  # Переопределяем rect для меньшего размера
            self.level_buttons.append(btn)

    def show(self, screen):
        active = True
        selected_level = None
        scroll_offset = 0  # смещение прокрутки

        while active:
            screen.fill(BLACK)

            # Заголовок
            font = pygame.font.Font("Fonts/Monocraft.otf", 40)
            title = font.render("ТАБЛИЦА ЛИДЕРОВ", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

            # Кнопки
            self.all_button.draw(screen)
            for btn in self.level_buttons:
                btn.draw(screen)
            self.back_button.draw(screen)

            # Отображение рекордов
            if selected_level is not None:
                self.display_records(screen, selected_level, scroll_offset)
            elif selected_level == 0:
                self.display_records(screen, None, scroll_offset)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.is_clicked(pygame.mouse.get_pos()):
                        active = False

                    if self.all_button.is_clicked(pygame.mouse.get_pos()):
                        selected_level = 0

                    for i, btn in enumerate(self.level_buttons, 1):
                        if btn.is_clicked(pygame.mouse.get_pos()):
                            selected_level = i

                # Прокрутка колесиком мыши
                if event.type == pygame.MOUSEWHEEL:
                    scroll_offset += event.y * 30
                    scroll_offset = max(min(scroll_offset, 0), -1000)  # ограничим прокрутку

            pygame.display.flip()

    def display_records(self, screen, level=None, scroll_offset=0):
        if level == 0:
            records = self.records_db.get_top_records(limit=100)
            title = "ЛУЧШИЕ РЕЗУЛЬТАТЫ (ВСЕ УРОВНИ)"
        else:
            records = self.records_db.get_top_records(level=level, limit=100)
            title = f"ЛУЧШИЕ РЕЗУЛЬТАТЫ (УРОВЕНЬ {level})"

        font_title = pygame.font.SysFont(None, 36)
        font = pygame.font.SysFont(None, 28)

        # Заголовок таблицы
        title_text = font_title.render(title, True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 250))

        # Заголовки
        headers = ["Место", "Игрок", "Время", "Уровень", "Дата"]
        col_positions = [70, 160, 330, 480, 600]
        for i, header in enumerate(headers):
            text = font.render(header, True, WHITE)
            screen.blit(text, (col_positions[i], 300))

        # Таблица
        if not records:
            text = font.render("Нет записей", True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 350))
        else:
            start_y = 340 + scroll_offset
            for i, record in enumerate(records, 1):
                player_name, time, lvl, date = record
                date_str = date.split()[0]

                # Формат времени: мм:сс:мс
                try:
                    time = float(time)
                except ValueError:
                    time = 0.0  # если вдруг не получится преобразовать

                minutes = int(time // 60)
                seconds = int(time % 60)
                milliseconds = int((time % 1) * 1000)

                time_str = f"{minutes:02d}:{seconds:02d}:{milliseconds:03d}"

                row_data = [str(i), player_name[:12], time_str, str(lvl), date_str]
                for j, data in enumerate(row_data):
                    text = font.render(data, True, WHITE)
                    screen.blit(text, (col_positions[j], start_y + i * 35))
