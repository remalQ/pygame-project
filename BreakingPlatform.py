import pygame


class BreakingPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, break_time=10000, reset_time=3000):
        super().__init__()
        self.original_image = pygame.Surface((width, height))
        self.original_image.fill((200, 100, 100))  # Красно-розовый
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))

        self.break_time = break_time
        self.reset_time = reset_time  # Время, через которое платформа восстанавливается
        self.initial_pos = (x, y)

        # Логические флаги
        self.timer_started = False
        self.break_start_time = None
        self.is_broken = False
        self.reset_start_time = None

    def update(self, player):
        if self.is_broken:
            # Если платформа сломана, проверяем время восстановления
            if self.reset_start_time is None:
                self.reset_start_time = pygame.time.get_ticks()
            else:
                elapsed = pygame.time.get_ticks() - self.reset_start_time
                if elapsed >= self.reset_time:
                    self.reset()
            return

        # Если игрок стоит на платформе
        if self.rect.colliderect(player.rect):
            if not self.timer_started:
                self.break_start_time = pygame.time.get_ticks()
                self.timer_started = True
            else:
                elapsed = pygame.time.get_ticks() - self.break_start_time
                if elapsed >= self.break_time:
                    self.breaking()
        else:
            # Если игрок ушел — сброс таймера
            self.timer_started = False
            self.break_start_time = None

    def breaking(self):
        self.is_broken = True
        self.image.set_alpha(0)  # Делаем невидимой
        self.rect.size = (0, 0)  # Отключаем коллизию

    def reset(self):
        self.is_broken = False
        self.timer_started = False
        self.break_start_time = None
        self.image = self.original_image.copy()
        self.image.set_alpha(255)
        self.rect = self.image.get_rect(topleft=self.initial_pos)
        self.reset_start_time = None  # Сбрасываем таймер восстановления
