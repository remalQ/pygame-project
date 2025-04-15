import pygame
import sys
from Button import Button
from Const_Values import *


class HelpMenu:
    def show(self, screen):
        help_active = True
        back_button = Button("Назад", WIDTH // 2, HEIGHT - 100, GRAY, WHITE)
        font = pygame.font.Font("Fonts/Monocraft.otf", 24)

        help_text = [
            "Добро пожаловать в платформер!",
            "Цель: дойти до двери, собирая монеты.",
            "",
            "Управление:",
            "← → — движение влево/вправо",
            "↑ или SPACE — прыжок",
            "ESC — пауза",
            "",
            "Избегайте ловушек и собирайте все монеты!",
        ]

        while help_active:
            screen.fill(BLACK)

            for i, line in enumerate(help_text):
                text_surface = font.render(line, True, WHITE)
                screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, 50 + i * 30))

            back_button.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_clicked(pygame.mouse.get_pos()):
                        help_active = False

            pygame.display.flip()
