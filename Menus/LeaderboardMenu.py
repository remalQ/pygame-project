from Button import Button
from Const_Values import *


class LeaderboardMenu:
    def __init__(self, records_db):
        self.records_db = records_db
        self.level_buttons = []

        # Создаем кнопки
        self.all_button = Button("Все уровни", WIDTH // 2, 150, GRAY, LIGHT_GRAY)
        self.back_button = Button("Назад", WIDTH // 2, HEIGHT - 100, GRAY, LIGHT_GRAY)
        self.clear_button = Button("Очистить", WIDTH // 2, HEIGHT - 50, RED, LIGHT_RED)

        # Настройка кнопок уровней
        button_width = 70
        button_height = 40
        button_spacing = 50
        total_buttons = 8
        total_width_needed = total_buttons * button_width + (total_buttons - 1) * button_spacing
        start_x = (WIDTH - total_width_needed) // 2

        for i in range(1, 9):
            btn_x = start_x + (i - 1) * (button_width + button_spacing)
            btn = Button(f"Ур.{i}", btn_x + button_width // 2, 200, GRAY, LIGHT_GRAY)
            btn.rect = pygame.Rect(btn_x, 175, button_width, button_height)
            self.level_buttons.append(btn)

    def show(self, screen):
        active = True
        selected_level = None
        scroll_offset = 0
        max_records_to_display = 8

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
            self.clear_button.draw(screen)

            # Отображение рекордов
            if selected_level is not None:
                self.display_records(screen, selected_level, scroll_offset, max_records_to_display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.is_clicked(pygame.mouse.get_pos()):
                        active = False

                    if self.all_button.is_clicked(pygame.mouse.get_pos()):
                        selected_level = 0

                    if self.clear_button.is_clicked(pygame.mouse.get_pos()):
                        confirm = self.show_confirmation_dialog(screen)
                        if confirm:
                            self.records_db.clear_all_records()
                            selected_level = None

                    for i, btn in enumerate(self.level_buttons, 1):
                        if btn.is_clicked(pygame.mouse.get_pos()):
                            selected_level = i

                if event.type == pygame.MOUSEWHEEL:
                    scroll_offset += event.y * 30
                    if selected_level is not None:
                        records = self.records_db.get_top_records(
                            level=(None if selected_level == 0 else selected_level))
                        max_offset = max(0, len(records) - max_records_to_display) * 35
                        scroll_offset = max(min(scroll_offset, 0), -max_offset)

            pygame.display.flip()

    def show_confirmation_dialog(self, screen):
        """Показывает диалог подтверждения очистки"""
        font = pygame.font.SysFont(None, 36)
        dialog_active = True

        # Создаем поверхность для полупрозрачного фона
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))

        while dialog_active:
            # Рисуем основной экран
            screen.blit(overlay, (0, 0))

            # Текст вопроса
            question = font.render("Очистить все рекорды? Это действие нельзя отменить.", True, WHITE)
            screen.blit(question, (WIDTH // 2 - question.get_width() // 2, HEIGHT // 2 - 50))

            # Кнопки
            yes_btn = Button("Да", WIDTH // 2 - 100, HEIGHT // 2 + 20, RED, LIGHT_RED)
            no_btn = Button("Нет", WIDTH // 2 + 100, HEIGHT // 2 + 20, GRAY, LIGHT_GRAY)

            yes_btn.draw(screen)
            no_btn.draw(screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_btn.is_clicked(pygame.mouse.get_pos()):
                        return True
                    elif no_btn.is_clicked(pygame.mouse.get_pos()):
                        return False
                elif event.type == pygame.QUIT:
                    return False

    def display_records(self, screen, level=None, scroll_offset=0, max_records=15):
        """Отображение таблицы рекордов (без изменений)"""
        if level == 0:
            records = self.records_db.get_top_records(limit=100)
            title = "ЛУЧШИЕ РЕЗУЛЬТАТЫ (ВСЕ УРОВНИ)"
        else:
            records = self.records_db.get_top_records(level=level, limit=100)
            title = f"ЛУЧШИЕ РЕЗУЛЬТАТЫ (УРОВЕНЬ {level})"

        font_title = pygame.font.SysFont(None, 36)
        font = pygame.font.SysFont(None, 28)
        font_small = pygame.font.SysFont(None, 24)

        # Заголовок таблицы
        title_text = font_title.render(title, True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 250))

        # Определение ширины столбцов
        total_width = WIDTH - 40
        col_widths = [
            int(total_width * 0.1),  # Место
            int(total_width * 0.3),  # Игрок
            int(total_width * 0.25),  # Время (увеличено для читаемости)
            int(total_width * 0.1),  # Уровень
            int(total_width * 0.25)  # Дата
        ]

        # Позиции столбцов
        col_positions = [20]
        for i in range(1, len(col_widths)):
            col_positions.append(col_positions[i - 1] + col_widths[i - 1])

        # Заголовки столбцов
        headers = ["Место", "Игрок", "Время", "Уровень", "Дата"]
        for i, header in enumerate(headers):
            text = font.render(header, True, WHITE)
            screen.blit(text, (col_positions[i], 300))

        # Таблица с записями
        if not records:
            text = font.render("Нет записей", True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 350))
        else:
            start_y = 340 + scroll_offset

            for i, record in enumerate(records[:max_records], 1):
                if start_y + i * 35 > HEIGHT - 150:
                    continue

                player_name, time_str, lvl, date = record
                date_str = date.split()[0] if date else ""

                # Разбиваем время на компоненты (уже должно быть отформатировано в RecordsDB)
                # Если формат неправильный, показываем "00:00:000"
                time_parts = time_str.split(':') if isinstance(time_str, str) else []
                if len(time_parts) == 3:
                    formatted_time = f"{time_parts[0]}:{time_parts[1]}:{time_parts[2]}"
                else:
                    formatted_time = "00:00:000"

                row_data = [
                    str(i),
                    player_name,
                    formatted_time,
                    str(lvl),
                    date_str
                ]

                for j, data in enumerate(row_data):
                    current_font = font_small if j == 1 and len(player_name) > 12 else font
                    text = current_font.render(data, True, WHITE)

                    # Обрезаем текст если не помещается
                    if text.get_width() > col_widths[j]:
                        truncated = data
                        while current_font.size(truncated + "...")[0] > col_widths[j] and len(truncated) > 1:
                            truncated = truncated[:-1]
                        text = current_font.render(truncated + "...", True, WHITE)

                    screen.blit(text, (col_positions[j], start_y + i * 35))