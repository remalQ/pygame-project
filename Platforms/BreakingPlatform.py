import pygame
from Platforms.Platform import Platform

class BreakingPlatform(Platform):
    def __init__(self, x, y, width, height, image=None, break_time=300):
        """
        break_time: время до исчезновения платформы после касания (в мс)
        """
        super().__init__(x, y, width, height, image)
        self.original_image = self.image.copy()    # Сохраняем оригинальное изображение платформы
        self.break_time = break_time               # Время жизни после активации таймера
        self.timer_started = False                 # Флаг — запущен ли таймер исчезновения
        self.break_start_time = None               # Момент запуска таймера
        self.is_disappeared = False                # Флаг — исчезла ли платформа

    def update(self):
        """
        Проверяет, пора ли исчезнуть платформе (если таймер запущен)
        """
        if self.is_disappeared or not self.timer_started:
            return  # Уже исчезла или не активировалась — ничего не делаем
        elapsed = pygame.time.get_ticks() - self.break_start_time
        if elapsed >= self.break_time:
            self.disappear()  # Время вышло — исчезаем

    def disappear(self):
        """
        Делает платформу невидимой и убирает из групп (коллизий)
        """
        self.is_disappeared = True
        self.image.set_alpha(0)    # Платформа становится невидимой
        self.rect.height = 0       # Отключаем коллизию по высоте
        self.kill()                # Удаляем из всех групп

    def start_disappear_timer(self):
        """
        Запускает таймер исчезновения (однократно при первом касании)
        """
        if not self.timer_started:
            self.break_start_time = pygame.time.get_ticks()
            self.timer_started = True
