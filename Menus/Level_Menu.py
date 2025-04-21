import sys
import os
import pickle
import pygame
from Button import *
from World import World
from Create_Maps import TILE_SIZE
from Const_Values import *

class LevelMenu:
    def __init__(self, total_levels):
        self.buttons = []
        self.total_levels = total_levels
        self.preview_cache = {}
        self.unlocked_levels = 1  # Сбрасываем прогресс до первого уровня при создании объекта

    def is_level_unlocked(self, level):
        return level <= self.unlocked_levels

    def generate_real_preview(self, world_data, scale=0.4):
        level_width = len(world_data[0]) * TILE_SIZE
        level_height = len(world_data) * TILE_SIZE
        preview_surface = pygame.Surface((level_width, level_height))

        dummy_player = pygame.sprite.Sprite()
        dummy_player.rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)

        dummy_group = pygame.sprite.Group()
        world = World(world_data, dummy_group, dummy_group, dummy_player)
        world.draw(preview_surface)

        scaled_size = (int(level_width * scale), int(level_height * scale))
        return pygame.transform.scale(preview_surface, scaled_size)

    def show(self, screen):
        menu_active = True
        self.buttons = []
        self.preview_cache = {}  # Очищаем кэш при каждом открытии меню

        for i in range(1, self.total_levels + 1):
            if i <= self.unlocked_levels:
                button = Button(f"Уровень {i}", WIDTH // 3, HEIGHT // (self.total_levels + 1) * i, GRAY, WHITE)
            else:
                button = Button(f"Уровень {i}", WIDTH // 3, HEIGHT // (self.total_levels + 1) * i, DARK_GRAY, DARK_GRAY)
            self.buttons.append(button)

        hovered_button = None

        while menu_active:
            screen.fill(BLACK)
            mouse_pos = pygame.mouse.get_pos()
            hovered_button = None

            for i, button in enumerate(self.buttons):
                if button.rect.collidepoint(mouse_pos) and (i + 1) <= self.unlocked_levels:
                    hovered_button = i + 1
                button.draw(screen)

            if hovered_button:
                if hovered_button not in self.preview_cache:
                    level_path = f"Maps/level{hovered_button}.pkl"
                    if os.path.exists(level_path):
                        try:
                            with open(level_path, "rb") as f:
                                data = pickle.load(f)
                                if isinstance(data, list):
                                    preview = self.generate_real_preview(data)
                                    self.preview_cache[hovered_button] = preview
                        except Exception as e:
                            print(f"Ошибка при загрузке уровня {hovered_button}: {e}")
                            self.preview_cache[hovered_button] = None

                preview = self.preview_cache.get(hovered_button)
                if preview:
                    preview_x = WIDTH // 2 + 100
                    preview_y = HEIGHT // 4
                    screen.blit(preview, (preview_x, preview_y))

                    preview_rect = pygame.Rect(preview_x, preview_y, preview.get_width(), preview.get_height())
                    pygame.draw.rect(screen, WHITE, preview_rect, 3)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        if button.is_clicked(mouse_pos) and (i + 1) <= self.unlocked_levels:
                            return i + 1

            pygame.display.flip()

    def unlock_next_level(self, completed_level):
        if completed_level >= 1 and completed_level == self.unlocked_levels and completed_level < self.total_levels:
            self.unlocked_levels += 1
            print(f"Уровень {self.unlocked_levels} разблокирован")