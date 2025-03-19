import pygame

pygame.init()

WIDTH, HEIGHT = 1000, 800
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("I Hate This Game")
clock = pygame.time.Clock()

tile_size = 50
game_over = 0
level = 1
main_menu = True

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (169, 169, 169)
