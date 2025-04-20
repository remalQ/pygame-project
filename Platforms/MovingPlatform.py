import pygame
from Platforms.Platform import Platform


class MovingPlatform(Platform):
    def __init__(self, x, y, width, height, player, distance_trigger=100, move_offset=150, speed=2, image=None):
        """
        player: объект игрока с атрибутом rect
        distance_trigger: дистанция, с которой платформа активируется
        move_offset: на сколько пикселей уехать вправо (или влево)
        speed: скорость движения
        """
        super().__init__(x, y, width, height, image)
        self.start_pos = pygame.Vector2(x, y)
        self.end_pos = pygame.Vector2(x + move_offset, y)
        self.current_target = self.end_pos
        self.player = player
        self.distance_trigger = distance_trigger
        self.speed = speed

        self.position = pygame.Vector2(self.rect.topleft)
        self.activated = False
        self.reached_target = False

    def update(self, *args, **kwargs):
        if not self.activated:
            # Проверяем расстояние до игрока
            player_dist = self.player.rect.centerx - self.rect.centerx
            if abs(player_dist) <= self.distance_trigger:
                self.activated = True

        if self.activated and not self.reached_target:
            direction = self.current_target - self.position
            distance = direction.length()

            if distance < self.speed:
                self.position = self.current_target
                self.reached_target = True
            else:
                direction = direction.normalize()
                self.position += direction * self.speed

            self.rect.topleft = self.position.xy

