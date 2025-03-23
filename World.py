"""
Модуль World отвечает за создание игрового мира, загрузку платформ и дверей,
а также их последующую отрисовку на экране.
"""

from Const_Values import *
from Door import Door


## \brief Класс World
#
# Отвечает за создание игрового мира, загрузку плиток и дверей, а также их отрисовку.
class World:
    ## \brief Конструктор класса
    #
    # Инициализирует игровой мир, загружает плитки и двери на основе переданных данных.
    # @param data Двумерный массив, представляющий карту уровня (1 - платформа, 2 - дверь)
    # @param door_group Группа спрайтов дверей, используется для хранения дверей на уровне
    def __init__(self, data, door_group):
        self.tile_list = []  # Список платформ
        self.door_group = door_group  # Группа дверей
        block_img = pygame.image.load("img/platform1.png")  # Загружаем изображение платформы

        # Проход по строкам и столбцам массива уровня
        for row_count, row in enumerate(data):
            for col_count, tile in enumerate(row):
                if tile == 1:
                    # Создание платформы
                    img = pygame.transform.scale(block_img, (tile_size, tile_size))
                    img_rect = img.get_rect(topleft=(col_count * tile_size, row_count * tile_size))
                    self.tile_list.append((img, img_rect))
                elif tile == 2:
                    # Создание двери
                    door = Door(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    self.door_group.add(door)

    ## \brief Метод draw()
    #
    # Отрисовывает все платформы и двери на экране.
    # @param screen Экран, на котором будут отображаться элементы уровня
    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])  # Отрисовка платформ

        self.door_group.draw(screen)  # Отрисовка дверей
