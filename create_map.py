import pygame
import os

pygame.init()

WIDTH, HEIGHT = 1000, 800
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

tile_size = 50
maps = []
map_Widht, map_Height = WIDTH // tile_size, HEIGHT // tile_size

# Инициализация карты
for row in range(map_Height):
    line = [0] * map_Widht
    maps.append(line)

# Загрузка карты при старте (если файл существует)
if os.path.exists('map2.txt'):
    with open('map2.txt', 'r') as file:
        data = file.readlines()
        for row in range(min(map_Height, len(data))):
            maps[row] = list(map(int, data[row].strip().split()))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Сохранение карты в файл
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            with open('map2.txt', 'w') as file:
                for row in maps:
                    file.write(' '.join(map(str, row)) + '\n')

    # Обработка мыши
    mousePx, mousePy = pygame.mouse.get_pos()
    b1, b2, b3 = pygame.mouse.get_pressed()

    mouseRow, mouseCol = mousePy // tile_size, mousePx // tile_size

    if 0 <= mouseRow < map_Height and 0 <= mouseCol < map_Widht:
        if b1:
            maps[mouseRow][mouseCol] = 1
        elif b3:
            maps[mouseRow][mouseCol] = 0

    # Отрисовка карты
    screen.fill(pygame.Color('black'))
    for row in range(map_Height):
        for col in range(map_Widht):
            x, y = col * tile_size, row * tile_size

            if maps[row][col] == 1:
                pygame.draw.rect(screen, pygame.Color('gray'), (x, y, tile_size, tile_size))
            pygame.draw.rect(screen, pygame.Color('white'), (x, y, tile_size, tile_size), 1)  # Сетка

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
