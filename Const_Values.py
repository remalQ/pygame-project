import pygame

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 1600, 900
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("I Hate This Game")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Шрифты
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)