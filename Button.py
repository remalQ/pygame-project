from Const_Values import *  # Импорт необходимых констант


# Класс кнопки
class Button:
    """
    Класс, представляющий кнопку на экране.

    Атрибуты:
        text (str): Текст на кнопке.
        x (int): X-координата центра кнопки.
        y (int): Y-координата центра кнопки.
        color (tuple): Цвет кнопки в обычном состоянии (RGB).
        hover_color (tuple): Цвет кнопки при наведении мыши (RGB).
        font (pygame.font.Font): Шрифт для текста на кнопке.
        rect (pygame.Rect): Прямоугольник, определяющий область кнопки.

    Методы:
        draw(screen): Отображает кнопку на экране.
        is_clicked(mouse_pos): Проверяет, была ли нажата кнопка.
    """

    def __init__(self, text, x, y, color, hover_color):
        """
        Инициализирует кнопку с заданными параметрами.

        Аргументы:
            text (str): Текст на кнопке.
            x (int): X-координата центра кнопки.
            y (int): Y-координата центра кнопки.
            color (tuple): Цвет кнопки.
            hover_color (tuple): Цвет кнопки при наведении.
        """
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont(None, 40)  # Шрифт кнопки
        self.rect = pygame.Rect(x - 100, y - 25, 200, 50)  # Прямоугольник кнопки

    def draw(self, screen):
        """
        Отображает кнопку на экране.

        Аргументы:
            screen (pygame.Surface): Экран, на котором будет отображена кнопка.
        """
        mouse_pos = pygame.mouse.get_pos()  # Получаем позицию мыши
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color  # Меняем цвет при наведении
        pygame.draw.rect(screen, color, self.rect)  # Рисуем кнопку
        text_surf = self.font.render(self.text, True, BLACK)  # Рисуем текст
        screen.blit(text_surf, (self.x - text_surf.get_width() // 2, self.y - text_surf.get_height() // 2))

    def is_clicked(self, mouse_pos):
        """
        Проверяет, была ли нажата кнопка.

        Аргументы:
            mouse_pos (tuple): Позиция мыши в момент нажатия.

        Возвращает:
            bool: True, если кнопка была нажата, иначе False.
        """
        return self.rect.collidepoint(mouse_pos)  # Проверка, попадает ли позиция мыши в область кнопки
