from Const_Values import *

"""
Класс LinePlatform

Этот класс представляет платформу в виде линии. 
Используется для создания платформ, которые игрок может рисовать во время игры.
"""

class LinePlatform(pygame.sprite.Sprite):
    ## \brief Конструктор класса
    #
    # Создает линейную платформу между двумя точками.
    # @param start_pos Начальная точка платформы (x, y).
    # @param end_pos Конечная точка платформы (x, y).
    def __init__(self, start_pos, end_pos):
        super().__init__()
        self.start_pos = start_pos  # Начальная позиция линии
        self.end_pos = end_pos  # Конечная позиция линии
        self.image = pygame.Surface((1, 1))  # Минимальная поверхность, т.к. рисование будет через pygame.draw
        self.width = 10  # Толщина платформы
        self.color = (255, 255, 255)  # Цвет платформы (белый)
        self.create_polygon()  # Создание хитбокса платформы

    ## \brief Метод создания хитбокса платформы
    #
    # Создает многоугольник, представляющий платформу, и её ограничивающий прямоугольник.
    def create_polygon(self):
        self.hitbox_points = [
            (self.start_pos[0], self.start_pos[1]),
            (self.end_pos[0], self.end_pos[1]),
            (self.end_pos[0], self.end_pos[1] + self.width),
            (self.start_pos[0], self.start_pos[1] + self.width)
        ]

        # Определяем границы (bounding box) платформы
        min_x = min(self.start_pos[0], self.end_pos[0])
        min_y = min(self.start_pos[1], self.end_pos[1])
        max_x = max(self.start_pos[0], self.end_pos[0])
        max_y = max(self.start_pos[1], self.end_pos[1]) + self.width

        self.rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    ## \brief Метод обновления позиции платформы
    #
    # Позволяет изменять положение платформы, обновляя её хитбокс.
    # @param start_pos Новая начальная точка (x, y).
    # @param end_pos Новая конечная точка (x, y).
    def update_position(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.create_polygon()  # Обновляем хитбокс платформы

    ## \brief Метод отрисовки платформы
    #
    # Отображает платформу как многоугольник на экране.
    # @param screen Экран, на котором будет нарисована платформа.
    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.hitbox_points)  # Рисуем платформу

    ## \brief Метод проверки коллизии с игроком
    #
    # Проверяет, находится ли игрок на платформе.
    # @param player Игрок, для которого проверяется коллизия.
    def check_collision(self, player):
        player_hitbox = pygame.Rect(player.rect.x, player.rect.y, player.rect.width, player.rect.height)

        if collidepolygon(player_hitbox, self.hitbox_points):  # Проверяем пересечение с платформой
            player.on_ground = True  # Устанавливаем флаг, что игрок на платформе
            player.rect.y = self.start_pos[1] - player.rect.height  # Корректируем положение игрока


## \brief Функция проверки пересечения прямоугольника и многоугольника
#
# Проверяет, пересекается ли прямоугольник (игрок) с многоугольником (платформой).
# @param rect Прямоугольник (pygame.Rect), представляющий игрока.
# @param polygon Список точек многоугольника (платформы).
# @return True, если есть пересечение, иначе False.
def collidepolygon(rect, polygon):
    # Проверка ширины и высоты прямоугольника
    if rect.width <= 0 or rect.height <= 0:
        return False

    # Проверяем пересечение с каждой стороной многоугольника
    for i in range(len(polygon)):
        next_i = (i + 1) % len(polygon)

        line_start = polygon[i]
        line_end = polygon[next_i]

        # Создаем прямоугольник для текущей стороны многоугольника
        line_rect = pygame.Rect(line_start, (line_end[0] - line_start[0], line_end[1] - line_start[1]))

        if rect.colliderect(line_rect):  # Проверяем пересечение
            return True

    return False  # Если пересечений нет
