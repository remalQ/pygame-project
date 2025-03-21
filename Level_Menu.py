import sys
from Button import *


class LevelMenu:
    def __init__(self, total_levels):
        self.buttons = []
        self.total_levels = total_levels

    def show(self, screen):
        menu_active = True
        self.buttons = []
        for i in range(1, self.total_levels + 1):
            button = Button(f"Уровень {i}", WIDTH // 2, HEIGHT // 2 - 100 + i * 50, GRAY, WHITE)
            self.buttons.append(button)

        while menu_active:
            screen.fill(BLACK)
            for button in self.buttons:
                button.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        if button.is_clicked(pygame.mouse.get_pos()):
                            return i + 1  # Возвращаем выбранный уровень

            pygame.display.flip()

