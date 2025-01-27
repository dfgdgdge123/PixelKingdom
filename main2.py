import pygame
import sys
from intro_end import IntroScreen, GameOverScreen

pygame.init()

CELL_SIZE = 50


class MapLoader:
    def __init__(self, filename):
        self.map_data = self.load_map(filename)
        self.assets = {
            "L": pygame.image.load("map_assets/land.jpg"),
            "G": pygame.image.load("map_assets/grass.jpg"),
            "F": pygame.image.load("map_assets/fild.jpg"),
            "C": pygame.image.load("map_assets/castle_floor.jpg"),
            "S": pygame.image.load("map_assets/castle_walls.jpg"),
            "1": pygame.image.load("map_assets/three1.jpg"),
            "2": pygame.image.load("map_assets/three2.jpg"),
            "3": pygame.image.load("map_assets/three3.jpg"),
            "4": pygame.image.load("map_assets/three3.jpg"),
            "5": pygame.image.load("map_assets/three5.jpg"),
        }

    def load_map(self, filename):
        with open(filename, "r") as file:
            return [line.strip() for line in file]

    def draw_map(self, screen):
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                if cell in self.assets:
                    screen.blit(self.assets[cell], (x * CELL_SIZE, y * CELL_SIZE))

    def can_move(self, x, y, hero_width, hero_height):
        rows, cols = len(self.map_data), len(self.map_data[0])
        corners = [
            (x // CELL_SIZE, y // CELL_SIZE),
            ((x + hero_width) // CELL_SIZE, y // CELL_SIZE),
            (x // CELL_SIZE, (y + hero_height) // CELL_SIZE),
            ((x + hero_width) // CELL_SIZE, (y + hero_height) // CELL_SIZE),
        ]
        return all(0 <= cy < rows and 0 <= cx < cols and self.map_data[cy][cx] == "L" for cx, cy in corners)


class Hero:
    def __init__(self):
        self.stand_sprite = pygame.image.load("hero_assets/hero.png")
        self.image = self.stand_sprite
        self.rect = self.image.get_rect()
        self.frame = 0
        self.is_attacking = False  # Флаг атаки
        self.load_animations()

    def load_animations(self):
        img_run_d = pygame.image.load("hero_assets/_Run.png")
        img_run_a = pygame.image.load("hero_assets/inv_Run.png")
        img_run_ws = pygame.image.load("hero_assets/_CrouchAll.png")
        img_attack = pygame.image.load("hero_assets/_Attack.png")

        self.anim_run_d = [img_run_d.subsurface(x, 42, 28, 38) for x in range(42, 1124, 121)]
        self.anim_run_a = [img_run_a.subsurface(x, 42, 28, 38) for x in reversed(range(42, 1124, 121))]
        self.anim_run_ws = [img_run_ws.subsurface(x, 46, 31, 33) for x in range(42, 282, 120)]

        # Анимация атаки
        self.anim_l_attack = [img_attack.subsurface(36, 41, 70, 42),
                              img_attack.subsurface(170, 41, 70, 42),
                              img_attack.subsurface(289, 41, 70, 42),
                              img_attack.subsurface(411, 41, 70, 42),]

    def move(self, map_loader, keys):
        if self.is_attacking:
            return  # Во время атаки герой не двигается

        new_x, new_y = self.rect.x, self.rect.y

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            new_x -= 3
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_x += 3
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_y += 3
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            new_y -= 3

        if map_loader.can_move(new_x, self.rect.y, self.rect.width, self.rect.height):
            self.rect.x = new_x
        if map_loader.can_move(self.rect.x, new_y, self.rect.width, self.rect.height):
            self.rect.y = new_y

    def attack(self):
        """Запускает анимацию атаки."""
        if not self.is_attacking:
            self.is_attacking = True
            self.frame = 0

    def animate(self):
        """Анимация персонажа. Теперь вызывается из игрового цикла."""
        if self.is_attacking:
            if self.frame < len(self.anim_l_attack) - 1:
                self.frame += 0.2
            else:
                self.is_attacking = False
            self.image = self.anim_l_attack[int(self.frame)]
        else:
            self.image = self.stand_sprite


class Game:
    def __init__(self):
        pygame.init()
        self.map_loader = MapLoader("map.txt")
        self.screen_width = len(self.map_loader.map_data[0]) * CELL_SIZE
        self.screen_height = len(self.map_loader.map_data) * CELL_SIZE
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pixel Kingdom")
        self.castle = pygame.image.load('map_assets/castle.png')
        self.hero = Hero()
        self.clock = pygame.time.Clock()
        self.init_hero_position()

    def init_hero_position(self):
        for y, row in enumerate(self.map_loader.map_data):
            for x, cell in enumerate(row):
                if cell == "L":
                    self.hero.rect.topleft = (x * CELL_SIZE, y * CELL_SIZE)
                    return

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.hero.attack()

            keys = pygame.key.get_pressed()
            self.hero.move(self.map_loader, keys)
            self.hero.animate()

            self.screen.fill((124, 172, 46))
            self.map_loader.draw_map(self.screen)
            self.screen.blit(self.castle, (self.screen_width // 1.19, self.screen_height // 2.5))
            self.screen.blit(self.hero.image, self.hero.rect)

            self.clock.tick(60)
            pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
