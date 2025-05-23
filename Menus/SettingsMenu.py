import pygame
import sys
from Button import Button
from Const_Values import *

class SettingsMenu:
    def __init__(self, game):
        self.game = game
        self.music_volume = 0.5
        self.sound_volume = 0.5
        self.sound_effect = pygame.mixer.Sound('Sounds/jump.wav')
        pygame.mixer.music.set_volume(self.music_volume)
        self.sound_effect.set_volume(self.sound_volume)
        self.game.set_sound_volume(self.sound_volume)

    def draw_slider(self, screen, x, y, value, label, font):
        label_text = font.render(label, True, WHITE)
        screen.blit(label_text, (x - label_text.get_width() // 2, y - 40))
        track_rect = pygame.Rect(x - 100, y, 200, 10)
        pygame.draw.rect(screen, GRAY, track_rect, border_radius=5)
        handle_pos = x - 100 + int(value * 200)
        handle_rect = pygame.Rect(handle_pos - 10, y - 5, 20, 20)
        pygame.draw.rect(screen, WHITE, handle_rect, border_radius=10)
        volume_text = font.render(f"{int(value * 100)}%", True, WHITE)
        screen.blit(volume_text, (x - volume_text.get_width() // 2, y + 20))
        return track_rect, handle_rect

    def handle_slider(self, mouse_pos, mouse_pressed, track_rect, current_value):
        if track_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            relative_x = mouse_pos[0] - track_rect.left
            new_value = max(0.0, min(1.0, relative_x / track_rect.width))
            return new_value
        return current_value

    def show(self, screen):
        settings_active = True
        back_button = Button("Назад", WIDTH // 2, HEIGHT // 2 + 150, GRAY, WHITE)
        font = pygame.font.Font("Fonts/Monocraft.otf", 30)
        title_font = pygame.font.Font("Fonts/Monocraft.otf", 40)

        while settings_active:
            screen.fill(BLACK)
            title = title_font.render("Настройки звука", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 200))
            music_track, music_handle = self.draw_slider(screen, WIDTH // 2, HEIGHT // 2 - 50, self.music_volume, "Музыка", font)
            sound_track, sound_handle = self.draw_slider(screen, WIDTH // 2, HEIGHT // 2 + 50, self.sound_volume, "Звук", font)
            back_button.draw(screen)
            mouse_pressed = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_clicked(pygame.mouse.get_pos()):
                        settings_active = False

            mouse_pos = pygame.mouse.get_pos()
            self.music_volume = self.handle_slider(mouse_pos, mouse_pressed, music_track, self.music_volume)
            self.sound_volume = self.handle_slider(mouse_pos, mouse_pressed, sound_track, self.sound_volume)
            pygame.mixer.music.set_volume(self.music_volume)
            self.sound_effect.set_volume(self.sound_volume)
            self.game.set_sound_volume(self.sound_volume)

            pygame.display.flip()