from Const_Values import *


# Класс платформы в виде линии
class LinePlatform(pygame.sprite.Sprite):
    def __init__(self, start_pos, end_pos):
        super().__init__()
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.image = pygame.Surface((1, 1))  # Создаем минимальную поверхность
        self.width = 10  # Ширина платформы
        self.color = (255, 255, 255)  # Цвет платформы
        self.create_polygon()  # Создаем хитбокс в виде многоугольника

    def create_polygon(self):
        self.hitbox_points = [
            (self.start_pos[0], self.start_pos[1]),
            (self.end_pos[0], self.end_pos[1]),
            (self.end_pos[0], self.end_pos[1] + self.width),
            (self.start_pos[0], self.start_pos[1] + self.width)
        ]

        # Создаем bounding box
        min_x = min(self.start_pos[0], self.end_pos[0])
        min_y = min(self.start_pos[1], self.end_pos[1])
        max_x = max(self.start_pos[0], self.end_pos[0])
        max_y = max(self.start_pos[1], self.end_pos[1]) + self.width

        self.rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def update_position(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.create_polygon()  # Пересоздаем хитбокс при изменении позиции

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.hitbox_points)  # Рисуем платформу как многоугольник

    def check_collision(self, player):
        # Проверяем пересечение с игроком
        player_hitbox = pygame.Rect(player.rect.x, player.rect.y, player.rect.width, player.rect.height)

        if player_hitbox.collidepolygon(
                self.hitbox_points):  # Здесь нужно будет реализовать проверку коллизии с многоугольником
            player.on_ground = True  # Устанавливаем флаг, что игрок на платформе
            player.rect.y = self.start_pos[1] - player.rect.height  # Устанавливаем позицию игрока на платформу


# Добавьте метод collidepolygon для проверки коллизий
def collidepolygon(rect, polygon):
    # Проверка пересечения прямоугольника и многоугольника
    # Первая проверка: ширина и высота прямоугольника
    if rect.width <= 0 or rect.height <= 0:
        return False

    # Проверяем пересечение с каждой стороной многоугольника
    for i in range(len(polygon)):
        next_i = (i + 1) % len(polygon)

        line_start = polygon[i]
        line_end = polygon[next_i]

        # Создаём рект для текущей стороны многоугольника
        line_rect = pygame.Rect(line_start, (line_end[0] - line_start[0], line_end[1] - line_start[1]))

        if rect.colliderect(line_rect):
            return True  # Если есть пересечение, возвращаем True

    return False  # Если пересечения нет, возвращаем False
