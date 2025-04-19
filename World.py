"""
Модуль World отвечает за создание игрового мира, загрузку всех игровых объектов
(платформы, двери, шипы, монеты) и их отрисовку на экране.
"""

import pygame
from Create_Maps import TILE_SIZE
# from Spike import Spike
from Coin import Coin
from Door import Door
from BreakingPlatform import BreakingPlatform


class World:
    """Класс World создает игровой мир на основе загруженных данных и отрисовывает его."""

    def __init__(self, data, door_group, coin_group, breaking_platform_group):
        """
        Инициализирует игровой мир.

        :param data: Двумерный массив, представляющий карту уровня
        :param door_group: Группа спрайтов дверей
        :param coin_group: Группа спрайтов монет
        """
        self.tile_list = []  # Список платформ
        self.door_group = door_group  # Группа дверей
        self.coin_group = coin_group  # Группа монет
        self.breaking_platform_group = breaking_platform_group


        # Загрузка изображений для тайлов
        self.textures = {
            1: pygame.image.load("Assets/platform.png").convert_alpha(),  # Платформа
            4: None  # Монета (анимированная, загружается в классе Coin)
        }

        # Проход по данным уровня
        for row_count, row in enumerate(data):
            for col_count, tile in enumerate(row):
                x, y = col_count * TILE_SIZE, row_count * TILE_SIZE

                if tile == 1:  # Платформа
                    # загружаем изображение без масштабирования (если оно уже нужного размера)
                    img = self.textures[1]
                    if img.get_size() != (TILE_SIZE, TILE_SIZE):
                        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect(topleft=(x, y))
                    self.tile_list.append((img, img_rect))

                elif tile == 2:  # Дверь
                    # проверяем, что это верхний левый тайл двери (чтобы не создавать 4 двери)
                    if (row_count < len(data) - 1 and col_count < len(row) - 1 and
                            data[row_count][col_count + 1] == 2 and
                            data[row_count + 1][col_count] == 2 and
                            data[row_count + 1][col_count + 1] == 2):
                        # дверь для 1 тайла
                        door = Door(x, y)
                        self.door_group.add(door)
                        # помечаем остальные тайлы для подходящего размера (2*2)
                        data[row_count][col_count + 1] = 0
                        data[row_count + 1][col_count] = 0
                        data[row_count + 1][col_count + 1] = 0

                elif tile == 4:  # Монета
                    coin = Coin(x, y)
                    self.coin_group.add(coin)

                elif tile == 5:  # Ломающаяся платформа
                    platform = BreakingPlatform(x, y, TILE_SIZE, TILE_SIZE)
                    self.breaking_platform_group.add(platform)

    def draw(self, screen):
        """Отрисовывает все элементы мира"""
        # Отрисовка платформ
        for img, rect in self.tile_list:
            screen.blit(img, rect)

        # Отрисовка дверей
        self.door_group.draw(screen)

        self.coin_group.update()
        self.coin_group.draw(screen)
        self.breaking_platform_group.draw(screen)

    def res(self):
        """Сброс состояния объектов мира (например, платформ)"""
        for platform in self.breaking_platform_group:
            platform.reset()

