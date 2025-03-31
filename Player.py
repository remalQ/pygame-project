"""@package Player
Класс игрока
"""

from Const_Values import *

## \brief Описание класса
#
# В этом классе у главного героя прописаны все основные механики его поведения
# относительно окружающего мира

class Player:
    ## \brief Конструктор класса
    #
    # Инициализирует объект игрока и вызывает метод reset для установки начальных параметров
    # @param x Начальная координата X
    # @param y Начальная координата Y
    def __init__(self, x, y):
        self.reset(x, y)

    ## \brief Метод update()
    #
    # Метод update изменяет состояние игрока каждый игровой тик.
    # Обрабатывает нажатия клавиш, движение и анимацию игрока.
    # Реализует базовую систему коллизий с платформами.
    # @param game_over Статус игры (0 - игра продолжается, 1 - победа, -1 - поражение)
    # @param world Игровой мир, содержащий платформы
    # @param door_group Группа дверей, используемых для завершения уровня
    # @param screen Экран для отрисовки игрока
    # @return Возвращает обновленный статус игры
    def update(self, game_over, world, door_group, screen):
        dx = 0
        dy = 0
        walk_cooldown = 5

        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            self.in_air = True
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            if pygame.sprite.spritecollide(self, door_group, False):
                game_over = 1

            if self.rect.y > HEIGHT:
                game_over = -1
            self.rect.x += dx
            self.rect.y += dy

        screen.blit(self.image, self.rect)
        return game_over

    ## \brief Метод reset()
    #
    # Сбрасывает состояние игрока, загружает изображения для анимации и
    # устанавливает стартовые координаты
    # @param x Начальная координата X
    # @param y Начальная координата Y
    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0

        for num in range(1, 6):
            img_right = pygame.image.load(f'Assets/frame{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 60))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True
