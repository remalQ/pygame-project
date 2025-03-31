import pygame
import os
from Create_Maps import TILE_SIZE


class Coin(pygame.sprite.Sprite):
    """Класс для анимированных монет"""

    def __init__(self, x, y):
        super().__init__()
        self.animation_frames = []
        self.load_animation_frames()
        self.current_frame = 0
        self.animation_speed = 0.2
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collected = False

    def load_animation_frames(self):
        """Загружает все кадры анимации из папки Coins"""
        coins_dir = "Assets/Coins"
        frame_files = sorted([f for f in os.listdir(coins_dir) if f.endswith('.png')])

        for frame_file in frame_files:
            frame_path = os.path.join(coins_dir, frame_file)
            frame = pygame.image.load(frame_path).convert_alpha()
            frame = pygame.transform.scale(frame, (TILE_SIZE, TILE_SIZE))
            self.animation_frames.append(frame)

    def update(self):
        """Обновляет анимацию монеты"""
        if not self.collected:
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.animation_frames):
                self.current_frame = 0
            self.image = self.animation_frames[int(self.current_frame)]

    def collect(self):
        """Помечает монету как собранную"""
        self.collected = True
        self.kill()  # Удаляем из группы