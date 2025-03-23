import sys
from Button import *

"""
Класс LevelMenu

Меню выбора уровня, которое отображает кнопки с номерами уровней. 
Позволяет игроку выбрать уровень перед началом игры.
"""

class LevelMenu:
    ## \brief Конструктор класса
    #
    # Создает меню с кнопками для выбора уровня.
    # @param total_levels Общее количество доступных уровней.
    def __init__(self, total_levels):
        self.buttons = []  # Список кнопок уровней
        self.total_levels = total_levels  # Общее количество уровней

    ## \brief Метод отображения меню выбора уровня
    #
    # Отрисовывает меню с кнопками уровней и обрабатывает ввод пользователя.
    # @param screen Экран, на котором будет отображаться меню.
    # @return Номер выбранного уровня.
    def show(self, screen):
        menu_active = True
        self.buttons = []  # Очищаем список кнопок перед созданием новых

        # Создаем кнопки для каждого уровня
        for i in range(1, self.total_levels + 1):
            button = Button(f"Уровень {i}", WIDTH // 2, HEIGHT // 2 - 100 + i * 50, GRAY, WHITE)
            self.buttons.append(button)

        # Главный цикл меню
        while menu_active:
            screen.fill(BLACK)  # Заливка экрана черным цветом

            # Отрисовка кнопок
            for button in self.buttons:
                button.draw(screen)

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Закрытие окна
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Обработка кликов
                    for i, button in enumerate(self.buttons):
                        if button.is_clicked(pygame.mouse.get_pos()):  # Проверяем, нажата ли кнопка
                            return i + 1  # Возвращаем номер выбранного уровня

            pygame.display.flip()  # Обновляем экран
