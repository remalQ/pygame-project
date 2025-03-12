from Const_Values import *


class PlatformDrawer:
    def __init__(self, game):
        self.game = game
        self.drawing = False
        self.start_pos = None
        self.temp_platform = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                self.drawing = True
                self.start_pos = event.pos
                self.temp_platform = pygame.Rect(self.start_pos, (0, 10))  # Создаем временную платформу

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.drawing:
                self.drawing = False
                end_pos = event.pos
                width = end_pos[0] - self.start_pos[0]
                platform = Platform(self.start_pos[0], self.start_pos[1], width, 10)
                self.game.platforms.add(platform)
                self.game.all_sprites.add(platform)
                self.temp_platform = None

        elif event.type == pygame.MOUSEMOTION:
            if self.drawing:
                end_pos = event.pos
                self.temp_platform.width = end_pos[0] - self.start_pos[0]

    def draw(self, screen):
        if self.drawing and self.temp_platform:
            pygame.draw.rect(screen, WHITE, self.temp_platform)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft=(x, y))