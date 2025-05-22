import pygame
from Platforms.Platform import Platform

class BouncingPlatform(Platform):
    def __init__(self, x, y, width, height, image=None, bounce_strength=15, side_push=10):
        """
        bounce_strength: Сила подбрасывания вверх/вниз (в пикселях за кадр)
        side_push: Сила отталкивания в стороны (в пикселях за кадр)
        """
        super().__init__(x, y, width, height, image)
        self.bounce_strength = bounce_strength
        self.side_push = side_push

    def apply_bounce(self, player):
        """
        Применяет эффект подбрасывания или отталкивания в зависимости от стороны столкновения.
        Возвращает корректировки dx, dy для игрока.
        """
        dx, dy = 0, 0
        player_rect = player.rect
        platform_rect = self.rect

        # Вычисляем пересечения по каждой стороне
        overlap_left = player_rect.right - platform_rect.left
        overlap_right = platform_rect.right - player_rect.left
        overlap_top = player_rect.bottom - platform_rect.top
        overlap_bottom = platform_rect.bottom - player_rect.top

        # Находим минимальное пересечение для определения стороны столкновения
        overlaps = [
            (abs(overlap_left), 'left', overlap_left),
            (abs(overlap_right), 'right', overlap_right),
            (abs(overlap_top), 'top', overlap_top),
            (abs(overlap_bottom), 'bottom', overlap_bottom)
        ]
        min_overlap = min(overlaps, key=lambda x: x[0])
        side, overlap_value = min_overlap[1], min_overlap[2]

        if side == 'top' and (player.vel_y >= 0 or player.fall_speed >= 0):
            # Столкновение сверху
            dy = platform_rect.top - player_rect.bottom
            player.vel_y = -self.bounce_strength
            player.fall_speed = -self.bounce_strength
            player.in_air = True
            player.falling_mode = False
        elif side == 'bottom' and (player.vel_y <= 0 or player.fall_speed <= 0):
            # Столкновение снизу
            dy = platform_rect.bottom - player_rect.top
            player.vel_y = self.bounce_strength
            player.fall_speed = self.bounce_strength
            player.in_air = True
        elif side == 'left' and player.vel_x >= 0:
            # Столкновение слева
            dx = platform_rect.left - player_rect.right
            player.vel_x = -self.side_push
        elif side == 'right' and player.vel_x <= 0:
            # Столкновение справа
            dx = platform_rect.right - player_rect.left
            player.vel_x = self.side_push

        return dx, dy