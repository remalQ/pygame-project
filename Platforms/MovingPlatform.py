import pygame
from Platforms.Platform import Platform

class MovingPlatform(Platform):
    def __init__(self, x, y, width, height, player, distance_trigger=100, move_offset=150, speed=2, image=None):
        """
        player: объект игрока для определения дистанции активации
        distance_trigger: расстояние, при котором платформа начинает двигаться
        move_offset: смещение, на которое платформа поедет (вправо)
        speed: скорость движения платформы
        """
        super().__init__(x, y, width, height, image)
        self.start_pos = pygame.Vector2(x, y)                       # Стартовая позиция платформы
        self.end_pos = pygame.Vector2(x + move_offset, y)           # Конечная позиция (по умолчанию вправо)
        self.current_target = self.end_pos                          # Куда сейчас движется платформа
        self.player = player
        self.distance_trigger = distance_trigger
        self.speed = speed

        self.position = pygame.Vector2(self.rect.topleft)           # Текущее положение платформы
        self.activated = False                                      # Флаг: активна ли платформа
        self.reached_target = False                                 # Флаг: доехала ли платформа

    def update(self, *args, **kwargs):
        """
        Проверяет, нужно ли активировать платформу и перемещает её
        """
        if not self.activated:
            # Если игрок близко — активируем движение платформы
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
            self.rect.topleft = self.position.xy  # Перемещаем платформу
