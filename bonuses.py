import pygame


class Bonus(pygame.sprite.Sprite):
    """Класс бонуса, который может быть подобран героем."""

    def __init__(self, image_path, x, y, effect):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.effect = effect  # Тип бонуса

    def apply(self, hero):
        """Применение бонуса к герою."""
        if self.effect == "speed":
            hero.speed = 4
            hero.speed_effect_time = pygame.time.get_ticks()
        elif self.effect == "health" and hero.lives < 10:  # Добавляем жизнь
            if hero.lives == 4.5:
                hero.lives = 5
            else:
                hero.lives += 1
        elif self.effect == "attack":
            hero.attack_power = 2
            hero.attack_effect_time = pygame.time.get_ticks()

    def draw(self, screen):
        """Отрисовка бонуса."""
        screen.blit(self.image, self.rect)