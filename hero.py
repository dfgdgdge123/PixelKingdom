import pygame


class Hero:
    def __init__(self):
        self.stand_sprite = pygame.image.load("hero_assets/hero.png").subsurface(40, 40, 25, 40)
        self.image = self.stand_sprite
        self.rect = self.image.get_rect()
        self.attack_area = pygame.Rect(*self.rect.topleft, self.rect.h * 2, self.rect.h * 2)

        self.frame = 0
        self.is_r_attacking = False  # Флаг атаки
        self.is_l_attacking = False
        self.moving_direction = None  # Направление движения
        self.load_animations()

        self.bonuses = []
        self.speed = 3  # Базовая скорость героя
        self.speed_effect_time = None
        self.attack_power = 1  # Базовая сила атаки
        self.attack_effect_time = None
        self.lives = 5  # Количество жизней героя

    def load_animations(self):
        img_run_d = pygame.image.load("hero_assets/_Run.png")
        img_run_a = pygame.image.load("hero_assets/inv_Run.png")
        img_run_ws = pygame.image.load("hero_assets/_CrouchAll.png")
        img_attack = pygame.image.load("hero_assets/_Attack.png")
        img_l_attack = pygame.image.load("hero_assets/inv_Attack.png")

        self.anim_run_d = [img_run_d.subsurface(x, 42, 28, 38) for x in range(42, 1124, 120)]
        self.anim_run_a = [img_run_a.subsurface(x, 42, 28, 38) for x in reversed(range(42, 1124, 120))]
        self.anim_run_ws = [img_run_ws.subsurface(x, 46, 31, 33) for x in range(42, 282, 120)]

        self.anim_r_attack = [img_attack.subsurface(36, 43, 40, 37),
                              img_attack.subsurface(171, 37, 66, 43),
                              img_attack.subsurface(292, 45, 67, 35),
                              img_attack.subsurface(414, 43, 58, 36)]

        self.anim_l_attack = [img_l_attack.subsurface(404, 42, 39, 38),
                              img_l_attack.subsurface(242, 37, 67, 43),
                              img_l_attack.subsurface(122, 43, 66, 37),
                              img_l_attack.subsurface(7, 46, 62, 34)]

    def move(self, map_loader, keys):
        # if self.is_r_attacking or self.is_l_attacking:
        #     return  # Во время атаки герой не двигается

        new_x, new_y = self.rect.x, self.rect.y
        self.moving_direction = None  # Сбрасываем направление

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            new_x -= self.speed
            self.moving_direction = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_x += self.speed
            self.moving_direction = "right"
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_y += self.speed
            self.moving_direction = "down"
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            new_y -= self.speed
            self.moving_direction = "up"

        if map_loader.can_move(new_x, self.rect.y, self.rect.width, self.rect.height):
            self.rect.x = new_x
        if map_loader.can_move(self.rect.x, new_y, self.rect.width, self.rect.height):
            self.rect.y = new_y

    def attack_r(self):
        """Запускает анимацию атаки."""
        if not self.is_r_attacking:
            self.is_r_attacking = True
            self.frame = 0

    def attack_l(self):
        """Запускает анимацию атаки."""
        if not self.is_l_attacking:
            self.is_l_attacking = True
            self.frame = 0


    def animate(self):
        """Анимация персонажа с обновлением размеров хитбокса."""
        previous_center = self.rect.center  # Сохраняем центр перед сменой анимации

        if self.is_r_attacking:
            if self.frame < len(self.anim_r_attack) - 1:
                self.frame += 0.2
            else:
                self.is_r_attacking = False
            self.image = self.anim_r_attack[int(self.frame)]

        elif self.is_l_attacking:
            if self.frame < len(self.anim_l_attack) - 1:
                self.frame += 0.2
            else:
                self.is_l_attacking = False
            self.image = self.anim_l_attack[int(self.frame)]

        elif self.moving_direction == "right":
            self.frame = (self.frame + 0.1) % len(self.anim_run_d)
            self.image = self.anim_run_d[int(self.frame)]

        elif self.moving_direction == "left":
            self.frame = (self.frame + 0.1) % len(self.anim_run_a)
            self.image = self.anim_run_a[int(self.frame)]

        elif self.moving_direction in ["up", "down"]:
            self.frame = (self.frame + 0.1) % len(self.anim_run_ws)
            self.image = self.anim_run_ws[int(self.frame)]

        else:
            self.image = self.stand_sprite  # Если не двигается — стоит на месте

        # Обновляем `rect`, чтобы он соответствовал новому размеру `image`
        self.rect = self.image.get_rect()
        self.rect.center = previous_center  # Сохраняем центр, чтобы спрайт не дёргался
