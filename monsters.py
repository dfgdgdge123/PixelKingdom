import pygame
import random
from bonuses import Bonus


class Monster(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, speed, map_loader, anim_run, anim_death, anim_hit, anim_attack, game):
        super().__init__()
        self.spritesheet = pygame.image.load(image_path)
        self.rect = pygame.Rect(x, y, 46, 52)
        self.speed = speed
        self.map_loader = map_loader
        self.frame = 0
        self.frame_speed = 0.1
        self.moving = True

        self.game = game  # Ссылка на игру для добавления бонусов

        self.anim_run = anim_run
        self.anim_death = anim_death
        self.anim_hit = anim_hit
        self.anim_attack = anim_attack

        self.image = self.anim_run[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.animation_index = 0
        self.animation_timer = 0
        self.is_dead = False
        self.is_hit = False
        self.is_attacking = False
        self.death_frame = 0
        self.hit_frame = 0
        self.attack_frame = 0

        self.bonus_drop_chance = 0.8  # 20% вероятность дропа

    def move(self):
        if self.moving:
            next_x = self.rect.x + self.speed
            if self.can_move(next_x, self.rect.y):
                self.rect.x = next_x
            else:
                self.moving = False

    def can_move(self, x, y):
        cell_x = (x + self.rect.width) // 50
        cell_y = y // 50

        if 0 <= cell_y < len(self.map_loader.map_data) and 0 <= cell_x < len(self.map_loader.map_data[0]):
            return self.map_loader.map_data[int(cell_y)][int(cell_x)] != "C"
        return False

    # def animate(self):
    #     if self.moving:
    #         self.frame = (self.frame + self.frame_speed) % len(self.can_move)
    #         self.image = self.can_move[int(self.frame)]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.is_dead:
            self.death_frame += 0.2
            if self.death_frame >= len(self.anim_death):
                self.kill()
            else:
                self.image = self.anim_death[int(self.death_frame)]
        elif self.is_hit:
            self.hit_frame += 0.2
            if self.hit_frame >= len(self.anim_hit):
                self.is_hit = False
                self.hit_frame = 0
            else:
                self.image = self.anim_hit[int(self.hit_frame)]
        elif self.is_attacking:
            self.attack_frame += 0.2
            if self.attack_frame >= len(self.anim_attack):
                self.is_attacking = False
                self.attack_frame = 0
            else:
                self.image = self.anim_attack[int(self.attack_frame)]
        else:
            # self.rect.x += self.speed
            self.move()

            self.animation_timer += 1
            if self.animation_timer >= 5:
                self.animation_timer = 0
                self.animation_index = (self.animation_index + 1) % len(self.anim_run)
                self.image = self.anim_run[self.animation_index]

    def die(self):
        """Обрабатывает смерть монстра и шанс выпадения бонуса."""
        self.is_dead = True
        if random.random() < self.bonus_drop_chance:
            self.drop_bonus()

    def take_hit(self):
        self.is_hit = True

    def attack(self):
        self.is_attacking = True

    def drop_bonus(self):
        """Создаёт бонус в месте смерти монстра."""
        if isinstance(self, Sceleton):
            bonus = Bonus("hero_assets/bonus_hill.png", self.rect.x, self.rect.y, "health")
        elif isinstance(self, Goblin):
            bonus = Bonus("hero_assets/bonus_speed.png", self.rect.x, self.rect.y, "speed")
        elif isinstance(self, Eye) or isinstance(self, Mushroom):
            bonus = Bonus("hero_assets/bonus_attack.png", self.rect.x, self.rect.y, "attack")
        else:
            return

        self.game.bonuses.append(bonus)  # Добавляем бонус в игру


class Sceleton(Monster):
    def __init__(self, screen_width, screen_height, map_loader, speed=2, game=None):
        sprite_sheet = pygame.image.load("monsters_assets/skeleton/Walk.png")
        death_sheet = pygame.image.load("monsters_assets/skeleton/Death.png")
        hit_sheet = pygame.image.load("monsters_assets/skeleton/Hit.png")
        attack_sheet = pygame.image.load("monsters_assets/skeleton/Attack.png")

        anim_run = [sprite_sheet.subsurface(60, 50, 47, 54),
                    sprite_sheet.subsurface(210, 50, 47, 54),
                    sprite_sheet.subsurface(360, 50, 47, 54),
                    sprite_sheet.subsurface(510, 50, 47, 54)]

        anim_death = [death_sheet.subsurface(60, 50, 40, 55),
                      death_sheet.subsurface(205, 50, 40, 55),
                      death_sheet.subsurface(350, 50, 40, 55),
                      death_sheet.subsurface(500, 50, 40, 55)]

        anim_hit = [hit_sheet.subsurface(60, 50, 46, 52),
                    hit_sheet.subsurface(210, 50, 46, 52),
                    hit_sheet.subsurface(350, 50, 46, 52),
                    hit_sheet.subsurface(500, 50, 46, 52)]

        anim_attack = [attack_sheet.subsurface(60, 50, 47, 54),
                       attack_sheet.subsurface(210, 50, 47, 54),
                       attack_sheet.subsurface(360, 50, 47, 54),
                       attack_sheet.subsurface(510, 50, 47, 54)]

        super().__init__("monsters_assets/skeleton/Idle.png", 170, 400, speed,
                         map_loader, anim_run, anim_death, anim_hit, anim_attack, game)


class Eye(Monster):
    def __init__(self, screen_width, screen_height, map_loader, speed=2, game=None):
        sprite_sheet = pygame.image.load("monsters_assets/eye/Flight.png")
        death_sheet = pygame.image.load("monsters_assets/eye/Death.png")
        hit_sheet = pygame.image.load("monsters_assets/eye/Hit.png")
        attack_sheet = pygame.image.load("monsters_assets/eye/Attack.png")

        anim_run = [sprite_sheet.subsurface(60, 50, 47, 54),
                    sprite_sheet.subsurface(210, 50, 47, 54),
                    sprite_sheet.subsurface(360, 50, 47, 54),
                    sprite_sheet.subsurface(510, 50, 47, 54)]

        anim_death = [death_sheet.subsurface(60, 50, 40, 55),
                      death_sheet.subsurface(205, 50, 40, 55),
                      death_sheet.subsurface(350, 50, 40, 55),
                      death_sheet.subsurface(500, 50, 40, 55)]

        anim_hit = [hit_sheet.subsurface(60, 50, 46, 52),
                    hit_sheet.subsurface(210, 50, 46, 52),
                    hit_sheet.subsurface(350, 50, 46, 52),
                    hit_sheet.subsurface(500, 50, 46, 52)]

        anim_attack = [attack_sheet.subsurface(60, 50, 47, 54),
                       attack_sheet.subsurface(210, 50, 47, 54),
                       attack_sheet.subsurface(360, 50, 47, 54),
                       attack_sheet.subsurface(510, 50, 47, 54)]

        super().__init__("monsters_assets/eye/Flight.png", 170, 200, speed,
                         map_loader, anim_run, anim_death, anim_hit, anim_attack, game)


class Goblin(Monster):
    def __init__(self, screen_width, screen_height, map_loader, speed=2, game=None):
        sprite_sheet = pygame.image.load("monsters_assets/goblin/Run.png")
        death_sheet = pygame.image.load("monsters_assets/goblin/Death.png")
        hit_sheet = pygame.image.load("monsters_assets/goblin/Hit.png")
        attack_sheet = pygame.image.load("monsters_assets/goblin/Attack.png")

        anim_run = [sprite_sheet.subsurface(60, 50, 47, 54),
                    sprite_sheet.subsurface(210, 50, 47, 54),
                    sprite_sheet.subsurface(360, 50, 47, 54),
                    sprite_sheet.subsurface(510, 50, 47, 54)]

        anim_death = [death_sheet.subsurface(60, 50, 40, 55),
                      death_sheet.subsurface(205, 50, 40, 55),
                      death_sheet.subsurface(350, 50, 40, 55),
                      death_sheet.subsurface(500, 50, 40, 55)]

        anim_hit = [hit_sheet.subsurface(60, 50, 46, 52),
                    hit_sheet.subsurface(210, 50, 46, 52),
                    hit_sheet.subsurface(350, 50, 46, 52),
                    hit_sheet.subsurface(500, 50, 46, 52)]

        anim_attack = [attack_sheet.subsurface(60, 50, 47, 54),
                       attack_sheet.subsurface(210, 50, 47, 54),
                       attack_sheet.subsurface(360, 50, 47, 54),
                       attack_sheet.subsurface(510, 50, 47, 54)]

        super().__init__("monsters_assets/goblin/Idle.png", 170, 300, speed,
                         map_loader, anim_run, anim_death, anim_hit, anim_attack, game)


class Mushroom(Monster):
    def __init__(self, screen_width, screen_height, map_loader, speed=2, game=None):
        sprite_sheet = pygame.image.load("monsters_assets/mushroom/Run.png")
        death_sheet = pygame.image.load("monsters_assets/mushroom/Death.png")
        hit_sheet = pygame.image.load("monsters_assets/mushroom/Hit.png")
        attack_sheet = pygame.image.load("monsters_assets/mushroom/Attack.png")

        anim_run = [sprite_sheet.subsurface(60, 50, 47, 54),
                    sprite_sheet.subsurface(210, 50, 47, 54),
                    sprite_sheet.subsurface(360, 50, 47, 54),
                    sprite_sheet.subsurface(510, 50, 47, 54)]

        anim_death = [death_sheet.subsurface(60, 50, 40, 55),
                      death_sheet.subsurface(205, 50, 40, 55),
                      death_sheet.subsurface(350, 50, 40, 55),
                      death_sheet.subsurface(500, 50, 40, 55)]

        anim_hit = [hit_sheet.subsurface(60, 50, 46, 52),
                    hit_sheet.subsurface(210, 50, 46, 52),
                    hit_sheet.subsurface(350, 50, 46, 52),
                    hit_sheet.subsurface(500, 50, 46, 52)]

        anim_attack = [attack_sheet.subsurface(60, 50, 47, 54),
                       attack_sheet.subsurface(210, 50, 47, 54),
                       attack_sheet.subsurface(360, 50, 47, 54),
                       attack_sheet.subsurface(510, 50, 47, 54)]

        super().__init__("monsters_assets/mushroom/Idle.png", 170, 250, speed,
                         map_loader, anim_run, anim_death, anim_hit, anim_attack, game)