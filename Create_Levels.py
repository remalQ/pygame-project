from Platform import *
from Door import *


class Level:
    def __init__(self, platforms, door_position):
        self.platforms = [Platform(x, y, width, height) for x, y, width, height in platforms]
        self.door = Door(door_position[0], door_position[1])

    def get_objects(self):
        return self.platforms, self.door

class TimedLevel(Level):
    def __init__(self, platforms, door_position, time_limit):
        super().__init__(platforms, door_position)
        self.time_limit = time_limit  # Время на прохождение уровня в секундах
        self.start_time = pygame.time.get_ticks()  # Время начала уровня

    def get_remaining_time(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Прошедшее время в секундах
        remaining_time = max(0, self.time_limit - elapsed_time)  # Оставшееся время
        return remaining_time

    def is_time_up(self):
        return self.get_remaining_time() <= 0

# Пример создания уровней
level_1 = Level(
    platforms=[
        (0, HEIGHT - 50, WIDTH / 2 - 100, 50),  # Левая половина пола
        (WIDTH / 2 + 100, HEIGHT - 50, WIDTH / 2 - 100, 50),  # Правая половина пола
        (200, HEIGHT - 200, 100, 20),  # Платформа 1
        (500, HEIGHT - 150, 100, 20),  # Платформа 2
    ],
    door_position=(WIDTH - 100, HEIGHT - 150)  # Позиция двери
)

level_2 = Level(
    platforms=[
        (0, HEIGHT - 50, WIDTH / 2 - 50, 50),  # Левая половина пола
        (WIDTH / 2 + 50, HEIGHT - 50, WIDTH / 2 - 50, 50),  # Правая половина пола
        (300, HEIGHT - 250, 150, 20),  # Платформа 1
        (600, HEIGHT - 180, 120, 20),  # Платформа 2
    ],
    door_position=(WIDTH - 120, HEIGHT - 200)  # Позиция двери
)

level_3 = TimedLevel(
    platforms=[
        (0, HEIGHT - 50, WIDTH / 2 - 100, 50),  # Левая половина пола
        (WIDTH / 2 + 100, HEIGHT - 50, WIDTH / 2 - 100, 50),  # Правая половина пола
        (200, HEIGHT - 300, 100, 20),  # Платформа 1
        (500, HEIGHT - 250, 100, 20),  # Платформа 2
        (700, HEIGHT - 200, 100, 20),  # Платформа 3
    ],
    door_position=(WIDTH - 100, HEIGHT - 200),  # Позиция двери
    time_limit=30  # 30 секунд на прохождение уровня
)
