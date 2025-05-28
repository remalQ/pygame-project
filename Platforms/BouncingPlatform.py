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
        self.bounce_speed = bounce_speed          # Скорость вертикального отскока
        self.side_push_speed = side_push_speed    # Скорость горизонтального отскока
        self.deceleration = deceleration          # Замедление отскока

    def apply_bounce(self, player):
        """
        Реализует отскок игрока от платформы — строго по направлению столкновения.
        Возвращает смещение dx, dy для корректного выхода из платформы.
        """
        dx, dy = 0, 0
        player_rect = player.rect
        platform_rect = self.rect

        # Вычисляем насколько прямоугольники перекрывают друг друга с каждой стороны
        overlap_left = player_rect.right - platform_rect.left
        overlap_right = platform_rect.right - player_rect.left
        overlap_top = player_rect.bottom - platform_rect.top
        overlap_bottom = platform_rect.bottom - player_rect.top

        # Сохраняем абсолютные значения перекрытий и определяем сторону столкновения
        overlaps = [
            (abs(overlap_left), 'left', overlap_left),
            (abs(overlap_right), 'right', overlap_right),
            (abs(overlap_top), 'top', overlap_top),
            (abs(overlap_bottom), 'bottom', overlap_bottom)
        ]
        min_overlap = min(overlaps, key=lambda x: x[0])
        side, overlap_value = min_overlap[1], min_overlap[2]

        # В зависимости от стороны корректируем скорость и смещение игрока
        if side == 'top' and (player.vel_y >= 0 or getattr(player, "fall_speed", 0) >= 0):
            # Игрок падает сверху — отскок вверх
            dy = -overlap_value  # Сдвигаем игрока вверх, чтобы не застревал
            player.start_vertical_bounce(-self.bounce_speed, self.deceleration)
        elif side == 'bottom' and (player.vel_y <= 0 or getattr(player, "fall_speed", 0) <= 0):
            # Снизу — отскок вниз
            dy = overlap_value
            player.start_vertical_bounce(self.bounce_speed, self.deceleration)
        elif side == 'left' and player.vel_x >= 0:
            # Слева — отскок влево
            dx = -overlap_value
            player.start_horizontal_bounce(-self.side_push_speed, self.deceleration)
        elif side == 'right' and player.vel_x <= 0:
            # Справа — отскок вправо
            dx = overlap_value
            player.start_horizontal_bounce(self.side_push_speed, self.deceleration)

        # Возвращаем смещение, чтобы игрок не застревал в платформе
        return dx, dy
