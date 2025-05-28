import pygame

class TextInputBox:
    def __init__(self, x, y, width, height, font_size=32, initial_text=""):
        """Создаёт поле ввода текста"""
        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color('white')
        self.text = initial_text
        self.font = pygame.font.SysFont('Arial', font_size)
        self.active = False

    def handle_event(self, event):
        """Обрабатывает события ввода и клика мыши"""
        # Клик мышью — активировать поле
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        # Ввод текста — только если поле активно
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                # Возврат True если текст не пустой
                if self.text:
                    return True
                return False
            elif event.key == pygame.K_BACKSPACE:
                # Удаляем последний символ
                self.text = self.text[:-1]
            else:
                # Добавляем новый символ
                self.text += event.unicode
        return False

    def draw(self, screen):
        """Отрисовывает поле ввода на экране"""
        # Рисуем прямоугольник и текст внутри
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
