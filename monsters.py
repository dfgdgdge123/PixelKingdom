import pygame


class Monster(pygame.sprite.Sprite):
    """Базовый класс монстра, который двигается вправо и останавливается у стены (C)."""

    def __init__(self, image_path, x, y, speed, map_loader):
        super().__init__()
        self.spritesheet = pygame.image.load(image_path)
        self.rect = pygame.Rect(x, y, 46, 52)
        self.speed = speed  # Используем переданную скорость
        self.map_loader = map_loader
        self.frame = 0
        self.frame_speed = 0.1
        self.moving = True

        self.anim_move = [self.spritesheet.subsurface(i * 46, 50, 46, 52) for i in range(4)]
        self.image = self.anim_move[0]

    def move(self):
        if self.moving:
            next_x = self.rect.x + self.speed
            if self.can_move(next_x, self.rect.y):
                self.rect.x = next_x
                self.animate()
            else:
                self.moving = False

    def can_move(self, x, y):
        """Проверяет, можно ли двигаться (не столкнулся ли правым боком со стеной 'C')."""
        cell_x = (x + self.rect.width) // 50
        cell_y = y // 50

        if 0 <= cell_y < len(self.map_loader.map_data) and 0 <= cell_x < len(self.map_loader.map_data[0]):
            return self.map_loader.map_data[int(cell_y)][int(cell_x)] != "C"
        return False

    def animate(self):
        if self.moving:
            self.frame = (self.frame + self.frame_speed) % len(self.anim_move)
            self.image = self.anim_move[int(self.frame)]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Sceleton(Monster):
    def __init__(self, screen_width, screen_height, map_loader, speed=2):
        super().__init__("monsters_assets/skeleton/Idle.png", 170, 400, speed, map_loader)

        sprite_sheet = pygame.image.load("monsters_assets/skeleton/Walk.png")
        death_sheet = pygame.image.load("monsters_assets/skeleton/Death.png")
        hit_sheet = pygame.image.load("monsters_assets/skeleton/Hit.png")
        attack_sheet = pygame.image.load("monsters_assets/skeleton/Attack.png")

        self.anim_run = [sprite_sheet.subsurface(60, 50, 47, 54),
                         sprite_sheet.subsurface(210, 50, 47, 54),
                         sprite_sheet.subsurface(360, 50, 47, 54),
                         sprite_sheet.subsurface(510, 50, 47, 54)]

        self.anim_death = [death_sheet.subsurface(60, 50, 40, 55),
                           death_sheet.subsurface(205, 50, 40, 55),
                           death_sheet.subsurface(350, 50, 40, 55),
                           death_sheet.subsurface(500, 50, 40, 55), ]

        self.anim_hit = [hit_sheet.subsurface(60, 50, 46, 52),
                         hit_sheet.subsurface(210, 50, 46, 52),
                         hit_sheet.subsurface(350, 50, 46, 52),
                         hit_sheet.subsurface(500, 50, 46, 52), ]

        self.anim_attack = [attack_sheet.subsurface(60, 50, 47, 54),
                            attack_sheet.subsurface(210, 50, 47, 54),
                            attack_sheet.subsurface(360, 50, 47, 54),
                            attack_sheet.subsurface(510, 50, 47, 54)]

        self.image = self.anim_run[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (170, 400)

        self.animation_index = 0
        self.animation_timer = 0
        self.is_dead = False
        self.is_hit = False
        self.is_attacking = False  # Флаг атаки
        self.death_frame = 0
        self.hit_frame = 0
        self.attack_frame = 0

    def update(self):
        if self.is_dead:
            self.death_frame += 0.2
            if self.death_frame >= len(self.anim_death):
                self.kill()  # Удаляем скелета с карты
            else:
                self.image = self.anim_death[int(self.death_frame)]
        elif self.is_hit:
            self.hit_frame += 0.2
            if self.hit_frame >= len(self.anim_hit):
                self.is_hit = False  # Завершаем анимацию получения урона
                self.hit_frame = 0
            else:
                self.image = self.anim_hit[int(self.hit_frame)]
        elif self.is_attacking:
            self.attack_frame += 0.2
            if self.attack_frame >= len(self.anim_attack):
                self.is_attacking = False  # Завершаем анимацию атаки
                self.attack_frame = 0
            else:
                self.image = self.anim_attack[int(self.attack_frame)]
        else:
            self.rect.x += self.speed

            self.animation_timer += 1
            if self.animation_timer >= 5:
                self.animation_timer = 0
                self.animation_index = (self.animation_index + 1) % len(self.anim_run)
                self.image = self.anim_run[self.animation_index]

    def die(self):
        self.is_dead = True

    def take_hit(self):
        self.is_hit = True  # Запускаем анимацию получения урона

    def attack(self):
        self.is_attacking = True  # Запускаем анимацию атаки


class Eye(Monster):
    def __init__(self, screen_width, screen_height, map_loader, speed=2):
        super().__init__("monsters_assets/eye/Flight.png", 170, 400, speed, map_loader)

        sprite_sheet = pygame.image.load("monsters_assets/eye/Flight.png")
        death_sheet = pygame.image.load("monsters_assets/eye/Death.png")
        hit_sheet = pygame.image.load("monsters_assets/eye/Hit.png")
        attack_sheet = pygame.image.load("monsters_assets/eye/Attack.png")

        self.anim_run = [sprite_sheet.subsurface(60, 50, 47, 54),
                         sprite_sheet.subsurface(210, 50, 47, 54),
                         sprite_sheet.subsurface(360, 50, 47, 54),
                         sprite_sheet.subsurface(510, 50, 47, 54)]

        self.anim_death = [death_sheet.subsurface(60, 50, 40, 55),
                           death_sheet.subsurface(205, 50, 40, 55),
                           death_sheet.subsurface(350, 50, 40, 55),
                           death_sheet.subsurface(500, 50, 40, 55), ]

        self.anim_hit = [hit_sheet.subsurface(60, 50, 46, 52),
                         hit_sheet.subsurface(210, 50, 46, 52),
                         hit_sheet.subsurface(350, 50, 46, 52),
                         hit_sheet.subsurface(500, 50, 46, 52), ]

        self.anim_attack = [attack_sheet.subsurface(60, 50, 47, 54),
                            attack_sheet.subsurface(210, 50, 47, 54),
                            attack_sheet.subsurface(360, 50, 47, 54),
                            attack_sheet.subsurface(510, 50, 47, 54)]

        self.image = self.anim_run[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (170, 200)

        self.animation_index = 0
        self.animation_timer = 0
        self.is_dead = False
        self.is_hit = False
        self.is_attacking = False  # Флаг атаки
        self.death_frame = 0
        self.hit_frame = 0
        self.attack_frame = 0

    def update(self):
        if self.is_dead:
            self.death_frame += 0.2
            if self.death_frame >= len(self.anim_death):
                self.kill()  # Удаляем скелета с карты
            else:
                self.image = self.anim_death[int(self.death_frame)]
        elif self.is_hit:
            self.hit_frame += 0.2
            if self.hit_frame >= len(self.anim_hit):
                self.is_hit = False  # Завершаем анимацию получения урона
                self.hit_frame = 0
            else:
                self.image = self.anim_hit[int(self.hit_frame)]
        elif self.is_attacking:
            self.attack_frame += 0.2
            if self.attack_frame >= len(self.anim_attack):
                self.is_attacking = False  # Завершаем анимацию атаки
                self.attack_frame = 0
            else:
                self.image = self.anim_attack[int(self.attack_frame)]
        else:
            self.rect.x += self.speed

            self.animation_timer += 1
            if self.animation_timer >= 5:
                self.animation_timer = 0
                self.animation_index = (self.animation_index + 1) % len(self.anim_run)
                self.image = self.anim_run[self.animation_index]

    def die(self):
        self.is_dead = True

    def take_hit(self):
        self.is_hit = True  # Запускаем анимацию получения урона

    def attack(self):
        self.is_attacking = True  # Запускаем анимацию атаки


class Goblin(Monster):
    def __init__(self, screen_width, screen_height, map_loader, speed=2):
        super().__init__("monsters_assets/goblin/Idle.png", 170, 400, speed, map_loader)

        sprite_sheet = pygame.image.load("monsters_assets/goblin/Run.png")
        death_sheet = pygame.image.load("monsters_assets/goblin/Death.png")
        hit_sheet = pygame.image.load("monsters_assets/goblin/Hit.png")
        attack_sheet = pygame.image.load("monsters_assets/goblin/Attack.png")

        self.anim_run = [sprite_sheet.subsurface(60, 50, 47, 54),
                         sprite_sheet.subsurface(210, 50, 47, 54),
                         sprite_sheet.subsurface(360, 50, 47, 54),
                         sprite_sheet.subsurface(510, 50, 47, 54)]

        self.anim_death = [death_sheet.subsurface(60, 50, 40, 55),
                           death_sheet.subsurface(205, 50, 40, 55),
                           death_sheet.subsurface(350, 50, 40, 55),
                           death_sheet.subsurface(500, 50, 40, 55), ]

        self.anim_hit = [hit_sheet.subsurface(60, 50, 46, 52),
                         hit_sheet.subsurface(210, 50, 46, 52),
                         hit_sheet.subsurface(350, 50, 46, 52),
                         hit_sheet.subsurface(500, 50, 46, 52), ]

        self.anim_attack = [attack_sheet.subsurface(60, 50, 47, 54),
                            attack_sheet.subsurface(210, 50, 47, 54),
                            attack_sheet.subsurface(360, 50, 47, 54),
                            attack_sheet.subsurface(510, 50, 47, 54)]

        self.image = self.anim_run[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (170, 300)

        self.animation_index = 0
        self.animation_timer = 0
        self.is_dead = False
        self.is_hit = False
        self.is_attacking = False  # Флаг атаки
        self.death_frame = 0
        self.hit_frame = 0
        self.attack_frame = 0

    def update(self):
        if self.is_dead:
            self.death_frame += 0.2
            if self.death_frame >= len(self.anim_death):
                self.kill()  # Удаляем скелета с карты
            else:
                self.image = self.anim_death[int(self.death_frame)]
        elif self.is_hit:
            self.hit_frame += 0.2
            if self.hit_frame >= len(self.anim_hit):
                self.is_hit = False  # Завершаем анимацию получения урона
                self.hit_frame = 0
            else:
                self.image = self.anim_hit[int(self.hit_frame)]
        elif self.is_attacking:
            self.attack_frame += 0.2
            if self.attack_frame >= len(self.anim_attack):
                self.is_attacking = False  # Завершаем анимацию атаки
                self.attack_frame = 0
            else:
                self.image = self.anim_attack[int(self.attack_frame)]
        else:
            self.rect.x += self.speed

            self.animation_timer += 1
            if self.animation_timer >= 5:
                self.animation_timer = 0
                self.animation_index = (self.animation_index + 1) % len(self.anim_run)
                self.image = self.anim_run[self.animation_index]

    def die(self):
        self.is_dead = True

    def take_hit(self):
        self.is_hit = True  # Запускаем анимацию получения урона

    def attack(self):
        self.is_attacking = True  # Запускаем анимацию атаки


class Mushroom(Monster):
    def __init__(self, screen_width, screen_height, map_loader, speed=2):
        super().__init__("monsters_assets/mushroom/Idle.png", 170, 400, speed, map_loader)

        sprite_sheet = pygame.image.load("monsters_assets/mushroom/Run.png")
        death_sheet = pygame.image.load("monsters_assets/mushroom/Death.png")
        hit_sheet = pygame.image.load("monsters_assets/mushroom/Hit.png")
        attack_sheet = pygame.image.load("monsters_assets/mushroom/Attack.png")

        self.anim_run = [sprite_sheet.subsurface(60, 50, 47, 54),
                         sprite_sheet.subsurface(210, 50, 47, 54),
                         sprite_sheet.subsurface(360, 50, 47, 54),
                         sprite_sheet.subsurface(510, 50, 47, 54)]

        self.anim_death = [death_sheet.subsurface(60, 50, 40, 55),
                           death_sheet.subsurface(205, 50, 40, 55),
                           death_sheet.subsurface(350, 50, 40, 55),
                           death_sheet.subsurface(500, 50, 40, 55), ]

        self.anim_hit = [hit_sheet.subsurface(60, 50, 46, 52),
                         hit_sheet.subsurface(210, 50, 46, 52),
                         hit_sheet.subsurface(350, 50, 46, 52),
                         hit_sheet.subsurface(500, 50, 46, 52), ]

        self.anim_attack = [attack_sheet.subsurface(60, 50, 47, 54),
                            attack_sheet.subsurface(210, 50, 47, 54),
                            attack_sheet.subsurface(360, 50, 47, 54),
                            attack_sheet.subsurface(510, 50, 47, 54)]

        self.image = self.anim_run[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (170, 250)

        self.animation_index = 0
        self.animation_timer = 0
        self.is_dead = False
        self.is_hit = False
        self.is_attacking = False  # Флаг атаки
        self.death_frame = 0
        self.hit_frame = 0
        self.attack_frame = 0

    def update(self):
        if self.is_dead:
            self.death_frame += 0.2
            if self.death_frame >= len(self.anim_death):
                self.kill()  # Удаляем скелета с карты
            else:
                self.image = self.anim_death[int(self.death_frame)]
        elif self.is_hit:
            self.hit_frame += 0.2
            if self.hit_frame >= len(self.anim_hit):
                self.is_hit = False  # Завершаем анимацию получения урона
                self.hit_frame = 0
            else:
                self.image = self.anim_hit[int(self.hit_frame)]
        elif self.is_attacking:
            self.attack_frame += 0.2
            if self.attack_frame >= len(self.anim_attack):
                self.is_attacking = False  # Завершаем анимацию атаки
                self.attack_frame = 0
            else:
                self.image = self.anim_attack[int(self.attack_frame)]
        else:
            self.rect.x += self.speed

            self.animation_timer += 1
            if self.animation_timer >= 5:
                self.animation_timer = 0
                self.animation_index = (self.animation_index + 1) % len(self.anim_run)
                self.image = self.anim_run[self.animation_index]

    def die(self):
        self.is_dead = True

    def take_hit(self):
        self.is_hit = True  # Запускаем анимацию получения урона

    def attack(self):
        self.is_attacking = True  # Запускаем анимацию атаки
