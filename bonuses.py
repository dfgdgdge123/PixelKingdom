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
            hero.speed += 1
        elif self.effect == "health" and hero.lives < 10:  # Добавляем жизнь
            if hero.lives == 9.5:
                hero.lives = 10
            else:
                hero.lives += 1
        elif self.effect == "attack":

            hero.attack_power += 1

    def draw(self, screen):
        """Отрисовка бонуса."""
        screen.blit(self.image, self.rect)
