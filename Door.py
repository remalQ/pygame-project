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
        img = pygame.image.load('Assets/door1.jpg')  # Загружаем изображение двери
        self.image = pygame.transform.scale(img, (tile_size * 3, tile_size * 3))  # Масштабируем изображение
        self.rect = self.image.get_rect(bottomleft=(x, y + tile_size * 2))
