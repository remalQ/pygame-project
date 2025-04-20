import pygame
from Platform import Platform


class BreakingPlatform(Platform):
    def __init__(self, x, y, width, height, image=None, break_time=1000):
        super().__init__(x, y, width, height, image)

        self.original_image = self.image.copy()
        self.break_time = break_time  # Время до исчезновения после касания (в мс)
        self.timer_started = False
        self.break_start_time = None
        self.is_disappeared = False

    def update(self):
        if self.is_disappeared or not self.timer_started:
            return  # Либо уже исчезла, либо таймер не запущен

        elapsed = pygame.time.get_ticks() - self.break_start_time
        if elapsed >= self.break_time:
            self.disappear()

    def disappear(self):
        self.is_disappeared = True
        self.image.set_alpha(0)         # Сделать невидимой
        self.rect.height = 0            # Убрать коллизию по высоте
        self.kill()

    def start_disappear_timer(self):
        if not self.timer_started:
            self.break_start_time = pygame.time.get_ticks()
            self.timer_started = True

