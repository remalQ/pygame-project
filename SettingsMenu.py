import pygame
import sys
from Button import Button
from Const_Values import *


class SettingsMenu:
    def __init__(self):
        self.volume = 0.5  # начальное значение громкости (от 0.0 до 1.0)
        pygame.mixer.music.set_volume(self.volume)

    def show(self, screen):
        settings_active = True
        increase_button = Button("Громче", WIDTH // 2, HEIGHT // 2 - 50, GRAY, WHITE)
        decrease_button = Button("Тише", WIDTH // 2, HEIGHT // 2 + 50, GRAY, WHITE)
        back_button = Button("Назад", WIDTH // 2, HEIGHT // 2 + 150, GRAY, WHITE)

        font = pygame.font.Font("Fonts/Monocraft.otf", 30)

        while settings_active:
            screen.fill(BLACK)

            # Текст заголовка
            title = font.render("Настройки звука", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 150))

            # Показ текущей громкости
            volume_text = font.render(f"Громкость: {int(self.volume * 100)}%", True, WHITE)
            screen.blit(volume_text, (WIDTH // 2 - volume_text.get_width() // 2, HEIGHT // 2 - 100))

            increase_button.draw(screen)
            decrease_button.draw(screen)
            back_button.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if increase_button.is_clicked(pygame.mouse.get_pos()):
                        self.volume = min(1.0, self.volume + 0.1)
                        pygame.mixer.music.set_volume(self.volume)

                    elif decrease_button.is_clicked(pygame.mouse.get_pos()):
                        self.volume = max(0.0, self.volume - 0.1)
                        pygame.mixer.music.set_volume(self.volume)

                    elif back_button.is_clicked(pygame.mouse.get_pos()):
                        settings_active = False

            pygame.display.flip()
