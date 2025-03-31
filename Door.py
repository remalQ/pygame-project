from Const_Values import *

"""
Класс Door

Отвечает за создание и отображение дверей в игре. Дверь является спрайтом, который можно использовать для перехода между уровнями.
"""


class Door(pygame.sprite.Sprite):
    ## \brief Конструктор класса
    #
    # Инициализирует дверь, загружая изображение и устанавливая ее позицию.
    # @param x Позиция двери по оси X
    # @param y Позиция двери по оси Y
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load('Assets/door.png')  # Загружаем изображение двери
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))  # Масштабируем изображение
        self.rect = self.image.get_rect(topleft=(x, y))  # Устанавливаем прямоугольник, который будет определять позицию двери
