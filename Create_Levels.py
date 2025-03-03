from Platform import *
from Door import *


class Level:
    def __init__(self, platforms, door_position):
        self.platforms = [Platform(x, y, width, height) for x, y, width, height in platforms]
        self.door = Door(door_position[0], door_position[1])

    def get_objects(self):
        return self.platforms, self.door


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