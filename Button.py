from Const_Values import *


# Класс кнопки
class Button:
    def __init__(self, text, center_x, center_y, color, hover_color, padding_x=20, padding_y=10):
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.padding_x = padding_x  # Отступ по горизонтали
        self.padding_y = padding_y  # Отступ по вертикали

        # Создаём поверхность с текстом
        self.text_surface = small_font.render(self.text, True, BLACK)
        self.text_rect = self.text_surface.get_rect()

        # Рассчитываем размер кнопки на основе текста и отступов
        self.width = self.text_rect.width + 2 * self.padding_x
        self.height = self.text_rect.height + 2 * self.padding_y

        # Прямоугольник кнопки (центрируем)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (center_x, center_y)  # Центрируем кнопку
        self.hovered = False

    def draw(self, screen):
        # Отрисовка кнопки с учётом состояния hovered
        pygame.draw.rect(screen, self.hover_color if self.hovered else self.color, self.rect)
        # Центрируем текст внутри кнопки
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        self.check_hover(mouse_pos)
        return self.hovered