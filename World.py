"""
Модуль World отвечает за создание игрового мира, загрузку всех игровых объектов
(платформы, двери, шипы, монеты) и их отрисовку на экране.
"""

import pygame
from Create_Maps import TILE_SIZE
# from Spike import Spike
# from Coin import Coin
from Door import Door


class World:
    """
    Класс World создает игровой мир на основе загруженных данных и отрисовывает его.
    """

    def __init__(self, data, door_group):
        """
        Инициализирует игровой мир, загружает тайлы и игровые объекты на основе переданных данных.

        :param data: Двумерный массив, представляющий карту уровня.
        :param door_group: Группа спрайтов дверей.
        :param spike_group: Группа спрайтов шипов.
        :param coin_group: Группа спрайтов монет.
        """
        self.tile_list = []  # Список платформ
        self.door_group = door_group  # Группа дверей
        # self.spike_group = spike_group  # Группа шипов
        # self.coin_group = coin_group  # Группа монет

        # Загрузка изображений для тайлов
        self.textures = {
            1: pygame.image.load("img/platform1.png"),  # Платформа
            # 3: pygame.image.load("img/spike.png"),  # Шипы
            # 4: pygame.image.load("img/coin.png"),  # Монета
        }

        # Проход по строкам и столбцам массива уровня
        for row_count, row in enumerate(data):
            for col_count, tile in enumerate(row):
                x, y = col_count * TILE_SIZE, row_count * TILE_SIZE  # Координаты тайла

                if tile in self.textures:
                    # Загружаем изображение для тайла
                    img = pygame.transform.scale(self.textures[tile], (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect(topleft=(x, y))

                    if tile == 1:  # Платформа
                        self.tile_list.append((img, img_rect))
                    # elif tile == 3:  # Шипы
                    #     self.spike_group.add(Spike(x, y))
                    # elif tile == 4:  # Монета
                    #     self.coin_group.add(Coin(x, y))

                elif tile == 2:  # Дверь
                    door = Door(x, y - (TILE_SIZE // 2))
                    self.door_group.add(door)

    def draw(self, screen):
        """
        Отрисовывает все элементы мира на экране.

        :param screen: Поверхность, на которой будет отрисован уровень.
        """
        for img, rect in self.tile_list:
            screen.blit(img, rect)  # Отрисовка платформ

        self.door_group.draw(screen)  # Отрисовка дверей
        # self.spike_group.draw(screen)  # Отрисовка шипов
        # self.coin_group.draw(screen)  # Отрисовка монет
