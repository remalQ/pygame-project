import pygame

pygame.init()

bg_img = pygame.image.load('img/bg.png')

WIDTH, HEIGHT = 1000, 800
FPC = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("I Hate This Game")
clock = pygame.time.Clock()

tile_size = 50
game_over = 0
level = 1
max_levels = 2
main_menu = True

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
