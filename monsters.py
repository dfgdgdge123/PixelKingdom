import pygame


class Monster(pygame.sprite.Sprite):
    """Базовый класс монстра, который двигается вправо и останавливается у стены (C)."""
    def __init__(self, image_path, x, y, speed, map_loader):
        super().__init__()
        self.spritesheet = pygame.image.load(image_path)  # Загружаем весь спрайт-лист
        self.rect = pygame.Rect(x, y, 46, 52)
        self.speed = speed
        self.map_loader = map_loader
        self.frame = 0  # Индекс текущего кадра анимации
        self.frame_speed = 0.1  # Скорость анимации

        # Создаём список кадров анимации движения
        self.anim_move = [self.spritesheet.subsurface(i * 46, 50, 46, 52) for i in range(4)]
        self.image = self.anim_move[0]  # Первый кадр анимации

    def move(self):
        """Монстр движется вправо и проверяет столкновение с замком."""
        next_x = self.rect.x + self.speed
        if self.can_move(next_x, self.rect.y):  # Проверка столкновения с замком
            self.rect.x = next_x
            self.animate()  # Обновляем анимацию движения

    def can_move(self, x, y):
        """Проверяет, можно ли двигаться (не столкнулся ли правым боком со стеной 'C')."""
        cell_x, cell_y = int((x + self.rect.width) // 50), int(y // 50)  # Проверяем ПРАВЫЙ бок монстра
        if 0 <= cell_y < len(self.map_loader.map_data) and 0 <= cell_x < len(self.map_loader.map_data[0]):
            return self.map_loader.map_data[cell_y][cell_x] != "C"  # Останавливаем монстра у стены
        return True

    def animate(self):
        """Переключает кадры анимации движения."""
        self.frame = (self.frame + self.frame_speed) % len(self.anim_move)
        self.image = self.anim_move[int(self.frame)]

    def draw(self, screen):
        """Отрисовывает монстра."""
        screen.blit(self.image, self.rect)


class Sceleton(Monster):
    def __init__(self, screen_width, screen_height, map_loader):
        super().__init__("monsters_assets/skeleton/Idle.png", 170, 400, 2, map_loader)

        sprite_sheet = pygame.image.load("monsters_assets/skeleton/Walk.png")

        self.anim_run = [sprite_sheet.subsurface(60, 50, 47, 54),
                         sprite_sheet.subsurface(210, 50, 47, 54),
                         sprite_sheet.subsurface(360, 50, 47, 54),
                         sprite_sheet.subsurface(510, 50, 47, 54),]

        self.image = self.anim_run[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (170, 400)

        self.animation_index = 0
        self.animation_timer = 0

    def update(self):
        self.rect.x += self.speed  # Двигаем монстра вправо

        # Анимация бега
        self.animation_timer += 1
        if self.animation_timer >= 5:
            self.animation_timer = 0
            self.animation_index = (self.animation_index + 1) % len(self.anim_run)
            self.image = self.anim_run[self.animation_index]


class Eye(Monster):
    def __init__(self, screen_width, screen_height, map_loader):
        super().__init__("monsters_assets/eye/Flight.png", 170, 400, 2, map_loader)

        sprite_sheet = pygame.image.load("monsters_assets/eye/Flight.png")

        self.anim_run = [sprite_sheet.subsurface(55, 60, 45, 30),
                         sprite_sheet.subsurface(205, 60, 45, 30),
                         sprite_sheet.subsurface(360, 60, 45, 30),
                         sprite_sheet.subsurface(505, 60, 45, 30),
                         sprite_sheet.subsurface(655, 60, 45, 30),
                         sprite_sheet.subsurface(805, 60, 45, 30),
                         sprite_sheet.subsurface(955, 60, 45, 30),
                         sprite_sheet.subsurface(1105, 60, 45, 30),]

        self.image = self.anim_run[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (170, 200)

        self.animation_index = 0
        self.animation_timer = 0

    def update(self):
        self.rect.x += self.speed  # Двигаем монстра вправо

        # Анимация бега
        self.animation_timer += 1
        if self.animation_timer >= 5:
            self.animation_timer = 0
            self.animation_index = (self.animation_index + 1) % len(self.anim_run)
            self.image = self.anim_run[self.animation_index]


class Goblin(Monster):
    def __init__(self, screen_width, screen_height, map_loader):
        super().__init__("monsters_assets/goblin/Idle.png", 170, 400, 2, map_loader)

        sprite_sheet = pygame.image.load("monsters_assets/goblin/Run.png")

        self.anim_run = [sprite_sheet.subsurface(50, 60, 42, 42),
                         sprite_sheet.subsurface(205, 60, 42, 42),
                         sprite_sheet.subsurface(360, 60, 42, 42),
                         sprite_sheet.subsurface(510, 60, 42, 42),
                         sprite_sheet.subsurface(660, 60, 42, 42),
                         sprite_sheet.subsurface(810, 60, 42, 42),
                         sprite_sheet.subsurface(960, 60, 42, 42),
                         sprite_sheet.subsurface(1110, 60, 42, 42),]

        self.image = self.anim_run[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (170, 250)

        self.animation_index = 0
        self.animation_timer = 0

    def update(self):
        self.rect.x += self.speed  # Двигаем монстра вправо

        # Анимация бега
        self.animation_timer += 1
        if self.animation_timer >= 5:
            self.animation_timer = 0
            self.animation_index = (self.animation_index + 1) % len(self.anim_run)
            self.image = self.anim_run[self.animation_index]


class Mushroom(Monster):
    def __init__(self, screen_width, screen_height, map_loader):
        super().__init__("monsters_assets/mushroom/Idle.png", 170, 400, 2, map_loader)

        sprite_sheet = pygame.image.load("monsters_assets/mushroom/Run.png")

        self.anim_run = [sprite_sheet.subsurface(60, 60, 30, 40),
                         sprite_sheet.subsurface(210, 60, 30, 40),
                         sprite_sheet.subsurface(360, 60, 30, 40),
                         sprite_sheet.subsurface(510, 60, 30, 40),
                         sprite_sheet.subsurface(660, 60, 30, 40),
                         sprite_sheet.subsurface(810, 60, 30, 40),
                         sprite_sheet.subsurface(960, 60, 30, 40),
                         sprite_sheet.subsurface(1110, 60, 30, 40),]

        self.image = self.anim_run[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (170, 330)

        self.animation_index = 0
        self.animation_timer = 0

    def update(self):
        self.rect.x += self.speed  # Двигаем монстра вправо

        # Анимация бега
        self.animation_timer += 1
        if self.animation_timer >= 5:
            self.animation_timer = 0
            self.animation_index = (self.animation_index + 1) % len(self.anim_run)
            self.image = self.anim_run[self.animation_index]