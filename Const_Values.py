import pygame

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 1000, 800  # Размер экрана
FPS = 60  # Частота кадров

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("I Hate This Game")  # Заголовок окна
clock = pygame.time.Clock()  # Таймер для кадров

# Размер клетки
tile_size = 25

# Статус игры
game_over = 0  # Переменная для отслеживания состояния игры (0 - игра продолжается)
level = 1  # Текущий уровень
main_menu = True  # Флаг для отображения главного меню

# Цвета
WHITE = (255, 255, 255)  # Белый
BLACK = (0, 0, 0)  # Черный
RED = (200, 0, 0)  # Стандартный красный
LIGHT_RED = (255, 100, 100)  # Светло-красный для кнопки очистки
GREEN = (0, 255, 0)  # Зеленый
BLUE = (0, 0, 255)  # Синий
GRAY = (200, 200, 200)  # Серый
DARK_GRAY = (169, 169, 169)  # Темно-серый
LIGHT_GRAY = (200, 200, 200)
