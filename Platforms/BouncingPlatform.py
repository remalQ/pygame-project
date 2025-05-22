import pygame
from Platforms.Platform import Platform


class BouncingPlatform(Platform):
    def __init__(self, x, y, width, height, image=None,
                 bounce_speed=30, side_push_speed=20, deceleration=1):
        """
        bounce_speed: Начальная вертикальная скорость при отскоке
        side_push_speed: Начальная горизонтальная скорость при отскоке
        deceleration: Модуль замедления (единиц в кадр^2)
        """
        super().__init__(x, y, width, height, image)
        self.bounce_speed = bounce_speed
        self.side_push_speed = side_push_speed
        self.deceleration = deceleration

    def apply_bounce(self, player):
        dx, dy = 0, 0
        player_rect = player.rect
        platform_rect = self.rect

        # Определим перекрытия
        overlap_left = player_rect.right - platform_rect.left
        overlap_right = platform_rect.right - player_rect.left
        overlap_top = player_rect.bottom - platform_rect.top
        overlap_bottom = platform_rect.bottom - player_rect.top

        # Определим минимальное перекрытие и сторону столкновения
        overlaps = [
            (abs(overlap_left), 'left', overlap_left),
            (abs(overlap_right), 'right', overlap_right),
            (abs(overlap_top), 'top', overlap_top),
            (abs(overlap_bottom), 'bottom', overlap_bottom)
        ]
        min_overlap = min(overlaps, key=lambda x: x[0])
        side, overlap_value = min_overlap[1], min_overlap[2]

        if side == 'top' and (player.vel_y >= 0 or player.fall_speed >= 0):
            # Отскок вверх
            dy = -overlap_value
            player.start_vertical_bounce(-self.bounce_speed, self.deceleration)
        elif side == 'bottom' and (player.vel_y <= 0 or player.fall_speed <= 0):
            # Отскок вниз
            dy = overlap_value
            player.start_vertical_bounce(self.bounce_speed, self.deceleration)
        elif side == 'left' and player.vel_x >= 0:
            # Отскок влево
            dx = -overlap_value
            player.start_horizontal_bounce(-self.side_push_speed, self.deceleration)
        elif side == 'right' and player.vel_x <= 0:
            # Отскок вправо
            dx = overlap_value
            player.start_horizontal_bounce(self.side_push_speed, self.deceleration)

        return dx, dy
