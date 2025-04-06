"""@package Player
Класс игрока
"""

from Const_Values import *
from Create_Maps import TILE_SIZE


class Player:
    ## \brief Конструктор класса
    #
    # Инициализирует объект игрока и вызывает метод reset для установки начальных параметров
    # @param x Начальная координата X
    # @param y Начальная координата Y
    def __init__(self, x, y):
        self.reset(x, y)
        self.coins_collected = 0  # Счетчик собранных монет
        self.coin_image = pygame.image.load("Coins/Gold_1.png")  # Загружаем картинку монеты
        self.coin_image = pygame.transform.scale(self.coin_image, (40, 40))  # Изменяем размер

    ## \brief Метод update()
    #
    # Основной метод обновления состояния игрока каждый кадр
    # Обрабатывает ввод, физику, коллизии и анимации
    # @param game_over Текущее состояние игры
    # @param world Игровой мир с платформами
    # @param door_group Группа спрайтов дверей
    # @param coin_group Группа спрайтов монет
    # @param screen Экран для отрисовки
    # @return Обновленное состояние игры
    def update(self, game_over, world, door_group, coin_group, screen):
        dx = 0  # Изменение по X
        dy = 0  # Изменение по Y
        walk_cooldown = 5  # Задержка между кадрами анимации ходьбы

        if game_over == 0:
            # Обработка ввода с клавиатуры
            key = pygame.key.get_pressed()

            # Прыжок (только если не в воздухе и не прыгали)
            if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
                self.vel_y = -15  # Начальная скорость прыжка
                self.jumped = True
                # Устанавливаем спрайт прыжка в текущем направлении
                if self.direction == 1:
                    self.image = self.jump_image_right
                else:
                    self.image = self.jump_image_left

            # Сброс флага прыжка при отпускании пробела
            if not key[pygame.K_SPACE]:
                self.jumped = False

            # Движение влево
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
                # Если на земле - анимация ходьбы
                if not self.in_air and self.counter > walk_cooldown:
                    self.counter = 0
                    self.index = (self.index + 1) % len(self.images_left)
                    self.image = self.images_left[self.index]

            # Движение вправо
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
                # Если на земле - анимация ходьбы
                if not self.in_air and self.counter > walk_cooldown:
                    self.counter = 0
                    self.index = (self.index + 1) % len(self.images_right)
                    self.image = self.images_right[self.index]

            # Если персонаж в воздухе - всегда показываем спрайт прыжка
            if self.in_air:
                if self.direction == 1:
                    self.image = self.jump_image_right
                else:
                    self.image = self.jump_image_left
            # Если стоит на месте - показываем первый кадр анимации
            elif not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                else:
                    self.image = self.images_left[self.index]

            # Гравитация
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # Обработка коллизий с платформами
            self.in_air = True  # Предполагаем, что в воздухе, пока не найдем опору
            for tile in world.tile_list:
                # Коллизия по X
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                    dx = 0
                # Коллизия по Y
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                    # Удар головой
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # Приземление
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False
                        # Устанавливаем стандартный спрайт при приземлении
                        if self.direction == 1:
                            self.image = self.images_right[self.index]
                        else:
                            self.image = self.images_left[self.index]

            # Сбор монет
            collected_coins = pygame.sprite.spritecollide(self, coin_group, True)
            self.coins_collected += len(collected_coins)

            # Проверка на завершение уровня (дверь)
            if pygame.sprite.spritecollide(self, door_group, False):
                game_over = 1

            # Проверка на падение за экран
            if self.rect.y > HEIGHT:
                game_over = -1

            # Обновление позиции
            self.rect.x += dx
            self.rect.y += dy

        # Отрисовка персонажа
        screen.blit(self.image, self.rect)
        return game_over

    ## \brief Метод reset()
    #
    # Сбрасывает состояние игрока к начальному
    # @param x Начальная координата X
    # @param y Начальная координата Y
    def reset(self, x, y):
        self.images_right = []  # Кадры анимации вправо
        self.images_left = []   # Кадры анимации влево
        self.index = 0          # Текущий кадр анимации
        self.counter = 0        # Счетчик для анимации

        # Загрузка кадров анимации ходьбы
        for num in range(1, 5):
            img_right = pygame.image.load(f'Assets/frame{num}.png').convert_alpha()
            img_right = pygame.transform.scale(img_right, (80, 90))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        # Загрузка изображений для прыжка
        self.jump_image_right = pygame.image.load('Assets/frame_jump.png').convert_alpha()
        self.jump_image_right = pygame.transform.scale(self.jump_image_right, (80, 90))
        self.jump_image_left = pygame.transform.flip(self.jump_image_right, True, False)

        # Начальные параметры
        self.direction = 1  # Направление (1 - вправо, -1 - влево)
        self.image = self.images_right[self.index]  # Текущее изображение
        self.rect = self.image.get_rect()          # Прямоугольник для коллизий
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.in_air = True