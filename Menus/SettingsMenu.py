import pygame
import sys
from Button import Button
from Const_Values import *

class SettingsMenu:
    def __init__(self):
        # Инициализация начальных значений громкости
        self.music_volume = 0.5  # Начальная громкость музыки (от 0.0 до 1.0)
        self.sound_volume = 0.5  # Начальная громкость звуковых эффектов (от 0.0 до 1.0)
        pygame.mixer.music.set_volume(self.music_volume)  # Установка громкости фоновой музыки

    def draw_slider(self, screen, x, y, value, label, font):
        # Отрисовка ползунка для регулировки громкости
        label_text = font.render(label, True, WHITE)
        screen.blit(label_text, (x - label_text.get_width() // 2, y - 40))

        # Отрисовка дорожки ползунка
        track_rect = pygame.Rect(x - 100, y, 200, 10)
        pygame.draw.rect(screen, GRAY, track_rect, border_radius=5)

        # Отрисовка ручки ползунка
        handle_pos = x - 100 + int(value * 200)  # Преобразование значения 0.0-1.0 в позицию 0-200 пикселей
        handle_rect = pygame.Rect(handle_pos - 10, y - 5, 20, 20)
        pygame.draw.rect(screen, WHITE, handle_rect, border_radius=10)

        # Отрисовка текущего значения громкости в процентах
        volume_text = font.render(f"{int(value * 100)}%", True, WHITE)
        screen.blit(volume_text, (x - volume_text.get_width() // 2, y + 20))

        return track_rect, handle_rect

    def handle_slider(self, mouse_pos, mouse_pressed, track_rect, current_value):
        # Обработка взаимодействия с ползунком
        if track_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            # Если мышь находится на дорожке и нажата левая кнопка
            relative_x = mouse_pos[0] - track_rect.left  # Относительная позиция мыши на дорожке
            new_value = max(0.0, min(1.0, relative_x / track_rect.width))  # Новое значение (0.0-1.0)
            return new_value
        return current_value  # Возврат текущего значения, если нет взаимодействия

    def show(self, screen):
        settings_active = True
        back_button = Button("Назад", WIDTH // 2, HEIGHT // 2 + 150, GRAY, WHITE)
        font = pygame.font.Font("Fonts/Monocraft.otf", 30)
        title_font = pygame.font.Font("Fonts/Monocraft.otf", 40)

        while settings_active:
            screen.fill(BLACK)

            title = title_font.render("Настройки звука", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 200))

            # Отрисовка ползунков для музыки и звуков
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

            # Применение громкости музыки
            pygame.mixer.music.set_volume(self.music_volume)

            pygame.display.flip()