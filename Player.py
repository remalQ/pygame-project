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

    def update(self):
        # Гравитация
        if not self.on_ground:
            self.velocity_y += 0.5

        # Движение по вертикали
        self.rect.y += self.velocity_y

        # Движение по горизонтали
        self.rect.x += self.velocity_x

        # Ограничение выхода за пределы экрана по горизонтали
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def jump(self):
        if self.on_ground:
            self.velocity_y = -12
            self.on_ground = False
