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
        self.font = pygame.font.Font("Fonts/Monocraft.otf", 40)
        self.text_surf = self.font.render(text, True, color)
        self.rect = self.text_surf.get_rect(center=(x, y))

    def draw(self, screen):
        """
        Отображает кнопку на экране.

        Аргументы:
            screen (pygame.Surface): Экран, на котором будет отображена кнопка.
        """
        mouse_pos = pygame.mouse.get_pos()
        # Меняем цвет текста при наведении
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        text_surf = self.font.render(self.text, True, color)
        screen.blit(text_surf, text_surf.get_rect(center=(self.x, self.y)))

    def is_clicked(self, mouse_pos):
        """
        Проверяет, была ли нажата кнопка.

        Аргументы:
            mouse_pos (tuple): Позиция мыши в момент нажатия.

        Возвращает:
            bool: True, если кнопка была нажата, иначе False.
        """
        return self.rect.collidepoint(mouse_pos)  # Проверка, попадает ли позиция мыши в область кнопки
