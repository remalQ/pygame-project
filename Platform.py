from Const_Values import *

"""
Класс Platform

Этот класс представляет платформу, на которой может стоять игрок.
Платформы могут иметь разные размеры и используются в игровом мире.
"""


class Platform(pygame.sprite.Sprite):
    ## \brief Конструктор класса
    #
    # Создает объект платформы с заданными координатами и размерами.
    # @param x Координата X верхнего левого угла платформы.
    # @param y Координата Y верхнего левого угла платформы.
    # @param width Ширина платформы.
    # @param height Высота платформы.
    def __init__(self, x, y, width, height):
        super().__init__()  # Инициализация родительского класса Sprite
        self.image = pygame.Surface((width, height))  # Создание поверхности платформы
        self.image.fill(WHITE)  # Заливка платформы белым цветом
        self.rect = self.image.get_rect()  # Получение прямоугольника платформы
        self.rect.topleft = (x, y)  # Установка позиции платформы

    ## \brief Метод отрисовки платформы
    #
    # Отображает платформу на экране.
    # @param screen Экран, на котором будет нарисована платформа.
    def draw(self, screen):
        screen.blit(self.image, self.rect)  # Отрисовка платформы
