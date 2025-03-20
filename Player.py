from Const_Values import *


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, HEIGHT - 150)

        self.velocity_y = 0
        self.velocity_x = 0
        self.on_ground = False
        self.speed = 5
        self.gravity = 0.5
        self.jump_power = -12

    def update(self, platforms):
        """Обновление состояния игрока: гравитация, движение, столкновения"""
        # Применяем гравитацию
        if not self.on_ground:
            self.velocity_y += self.gravity
            if self.velocity_y > 10:  # Ограничение скорости падения
                self.velocity_y = 10

        # Сохраняем старую позицию перед проверкой столкновений
        old_y = self.rect.y

        # Движение по вертикали
        self.rect.y += self.velocity_y
        self.on_ground = False  # Сначала предполагаем, что игрок не на земле
        self.check_collisions(0, self.velocity_y, platforms)

        # Если игрок не двигался вниз, значит, он стоит на платформе
        if old_y < self.rect.y and self.velocity_y == 0:
            self.on_ground = True

        # Движение по горизонтали
        self.rect.x += self.velocity_x
        self.check_collisions(self.velocity_x, 0, platforms)

    def check_collisions(self, dx, dy, platforms):
        """Обрабатывает столкновения с платформами по горизонтали и вертикали"""
        for platform in platforms:
            if self.rect.colliderect(platform.rect):  # Если игрок столкнулся с платформой
                if dx > 0:  # Движение вправо
                    self.rect.right = platform.rect.left
                    self.velocity_x = 0
                elif dx < 0:  # Движение влево
                    self.rect.left = platform.rect.right
                    self.velocity_x = 0

                if dy > 0:  # Падение вниз
                    self.rect.bottom = platform.rect.top - 1
                    self.velocity_y = 0
                    self.on_ground = True  # Теперь точно знаем, что игрок стоит на платформе
                elif dy < 0:  # Прыжок вверх
                    self.rect.top = platform.rect.bottom + 1
                    self.velocity_y = 0

    def jump(self):
        """Игрок прыгает, только если стоит на платформе"""
        if self.on_ground:
            self.velocity_y = self.jump_power  # Улучшенный прыжок
            self.on_ground = False
