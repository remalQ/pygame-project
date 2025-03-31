"""
Модуль World отвечает за создание игрового мира, загрузку всех игровых объектов
(платформы, двери, шипы, монеты) и их отрисовку на экране.
"""

import pygame
from Create_Maps import TILE_SIZE
# from Spike import Spike
from Coin import Coin
from Door import Door


class World:
    """Класс World создает игровой мир на основе загруженных данных и отрисовывает его."""

    def __init__(self, data, door_group, coin_group):
        """
        Инициализирует игровой мир.

        :param data: Двумерный массив, представляющий карту уровня
        :param door_group: Группа спрайтов дверей
        :param coin_group: Группа спрайтов монет
        """
        self.tile_list = []  # Список платформ
        self.door_group = door_group  # Группа дверей
        self.coin_group = coin_group  # Группа монет

        # Загрузка изображений для тайлов
        self.textures = {
            1: pygame.image.load("Assets/platform1.png").convert_alpha(),  # Платформа
            4: None  # Монета (анимированная, загружается в классе Coin)
        }

        # Проход по данным уровня
        for row_count, row in enumerate(data):
            for col_count, tile in enumerate(row):
                x, y = col_count * TILE_SIZE, row_count * TILE_SIZE

                if tile == 1:  # Платформа
                    img = pygame.transform.scale(self.textures[1], (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect(topleft=(x, y))
                    self.tile_list.append((img, img_rect))

                elif tile == 2:  # Дверь
                    door = Door(x, y - (TILE_SIZE // 2))
                    self.door_group.add(door)

                elif tile == 4:  # Монета
                    coin = Coin(x, y)
                    self.coin_group.add(coin)

    def draw(self, screen):
        """Отрисовывает все элементы мира"""
        # Отрисовка платформ
        for img, rect in self.tile_list:
            screen.blit(img, rect)

        # Отрисовка дверей
        self.door_group.draw(screen)

        # Обновление и отрисовка монет
        self.coin_group.update()
        self.coin_group.draw(screen)