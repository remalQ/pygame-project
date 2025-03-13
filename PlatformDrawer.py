from LinePlatform import *


class PlatformDrawer:
    def __init__(self, game):
        self.game = game
        self.drawing = False
        self.start_pos = None
        self.temp_line = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                self.drawing = True
                self.start_pos = event.pos
                self.temp_line = LinePlatform(self.start_pos, self.start_pos)  # Создаем временную линию
                self.game.all_sprites.add(self.temp_line)  # Добавляем временную линию в спрайты

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.drawing:
                self.drawing = False
                end_pos = event.pos
                line_platform = LinePlatform(self.start_pos, end_pos)
                self.game.platforms.add(line_platform)
                self.game.all_sprites.add(line_platform)
                if self.temp_line:
                    self.temp_line.kill()
                    self.temp_line = None
                pygame.display.update()

        elif event.type == pygame.MOUSEMOTION:
            if self.drawing and self.temp_line:
                end_pos = event.pos
                self.temp_line.update_position(self.start_pos, end_pos)  # Обновляем временную линию

    def draw(self, screen):
        for platform in self.game.platforms:
            platform.draw(screen)
