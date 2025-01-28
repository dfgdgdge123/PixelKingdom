import pygame


class Sceleton(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load("monsters_assets/skeleton/Idle.png").subsurface(60, 50, 46, 52)
        self.rect = self.image.get_rect()
        self.rect.center = (170, 280)  # Размещаем монстра в центре экрана

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Eye(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load("monsters_assets/eye/Flight.png").subsurface(60, 50, 46, 52)
        self.rect = self.image.get_rect()
        self.rect.center = (170, 220)  # Размещаем монстра в центре экрана

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Goblin(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load("monsters_assets/goblin/Idle.png").subsurface(60, 50, 46, 52)
        self.rect = self.image.get_rect()
        self.rect.center = (170, 340)  # Размещаем монстра в центре экрана

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Mushroom(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load("monsters_assets/mushroom/Idle.png").subsurface(60, 50, 46, 52)
        self.rect = self.image.get_rect()
        self.rect.center = (170, 400)  # Размещаем монстра в центре экрана

    def draw(self, screen):
        screen.blit(self.image, self.rect)


