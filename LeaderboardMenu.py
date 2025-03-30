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

        while active:
            screen.fill(BLACK)

            # Заголовок
            font = pygame.font.SysFont(None, 60)
            title = font.render("ТАБЛИЦА ЛИДЕРОВ", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

            # Кнопки выбора уровня
            self.all_button.draw(screen)
            for btn in self.level_buttons:
                btn.draw(screen)
            self.back_button.draw(screen)

            # Отображение рекордов
            if selected_level is not None:
                self.display_records(screen, selected_level)
            elif selected_level == 0:  # Все уровни
                self.display_records(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.is_clicked(pygame.mouse.get_pos()):
                        active = False

                    if self.all_button.is_clicked(pygame.mouse.get_pos()):
                        selected_level = 0  # Показать все уровни

                    for i, btn in enumerate(self.level_buttons, 1):
                        if btn.is_clicked(pygame.mouse.get_pos()):
                            selected_level = i

            pygame.display.flip()

        return None

    def display_records(self, screen, level=None):
        if level == 0:
            records = self.records_db.get_top_records(limit=20)
            title = "ЛУЧШИЕ РЕЗУЛЬТАТЫ (ВСЕ УРОВНИ)"
        else:
            records = self.records_db.get_top_records(level=level)
            title = f"ЛУЧШИЕ РЕЗУЛЬТАТЫ (УРОВЕНЬ {level})"

        # Заголовок таблицы
        font = pygame.font.SysFont(None, 40)
        title_text = font.render(title, True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 250))

        # Заголовки столбцов
        font = pygame.font.SysFont(None, 30)
        headers = ["Место", "Игрок", "Время", "Уровень", "Дата"]
        for i, header in enumerate(headers):
            text = font.render(header, True, WHITE)
            screen.blit(text, (50 + i * 150, 300))

        # Записи рекордов
        if not records:
            text = font.render("Нет записей", True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 350))
        else:
            for i, record in enumerate(records[:10], 1):  # Ограничиваем 10 записями
                player_name, time, lvl, date = record
                date_str = date.split()[0]  # Берем только дату без времени

                # Форматируем время в секундах в минуты:секунды
                minutes = int(time // 60)
                seconds = int(time % 60)
                time_str = f"{minutes:02d}:{seconds:02d}"

                # Отображаем запись
                row_data = [str(i), player_name[:10], time_str, str(lvl), date_str]
                for j, data in enumerate(row_data):
                    text = font.render(data, True, WHITE)
                    screen.blit(text, (50 + j * 150, 350 + i * 40))