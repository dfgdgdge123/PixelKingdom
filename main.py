import random

import pygame
import sys
from intro_end import IntroScreen, GameOverScreen
from monsters import Sceleton, Eye, Goblin, Mushroom
from hero import Hero

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

    def is_wall(self, x, y):
        """ Проверяет, является ли клетка стеной 'C' """
        cell_x, cell_y = x // CELL_SIZE, y // CELL_SIZE
        if 0 <= cell_y < len(self.map_data) and 0 <= cell_x < len(self.map_data[0]):
            return self.map_data[cell_y][cell_x] == "C"
        return False


class Game:
    def __init__(self):
        pygame.init()
        self.map_loader = MapLoader("map.txt")
        self.screen_width = len(self.map_loader.map_data[0]) * CELL_SIZE
        self.screen_height = len(self.map_loader.map_data) * CELL_SIZE
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pixel Kingdom")

        self.heart_image = pygame.image.load("hero_assets/heart.png")
        self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))

        self.lives = 10  # Количество жизней героя

        self.castle = pygame.image.load('map_assets/castle.png')
        self.hero = Hero()
        self.clock = pygame.time.Clock()
        self.init_hero_position()

        # self.monsters = [
        #     Sceleton(self.screen_width, self.screen_height, self.map_loader, speed=1),
        #     Eye(self.screen_width, self.screen_height, self.map_loader, speed=1.5),
        #     Goblin(self.screen_width, self.screen_height, self.map_loader, speed=2),
        #     Mushroom(self.screen_width, self.screen_height, self.map_loader, speed=1.3),
        # ]

        self.monster_hits = {
            Sceleton: {"hits_to_kill": 5, "hit_count": {}},
            Eye: {"hits_to_kill": 3, "hit_count": {}},
            Goblin: {"hits_to_kill": 2, "hit_count": {}},
            Mushroom: {"hits_to_kill": 4, "hit_count": {}},
        }

        self.last_hit_time = 0
        self.hit_cooldown = 1500

        self.monsters = []
        self.spawn_time = 5000  # Интервал спавна в миллисекундах (5 секунд)
        self.last_spawn = pygame.time.get_ticks()

    def init_hero_position(self):
        # Находим середину карты
        mid_y = len(self.map_loader.map_data) // 2
        mid_x = len(self.map_loader.map_data[0]) // 2

        # Ищем ближайшую клетку 'L' вокруг середины карты
        for y in range(mid_y - 1, mid_y + 2):  # Проверяем три строки вокруг середины
            for x in range(mid_x - 1, mid_x + 2):  # Проверяем три столбца вокруг середины
                if 0 <= y < len(self.map_loader.map_data) and 0 <= x < len(self.map_loader.map_data[0]):
                    if self.map_loader.map_data[y][x] == "L":
                        self.hero.rect.topleft = (x * CELL_SIZE, y * CELL_SIZE)
                        return

        # Если не нашли клетку 'L' вокруг середины, ищем первую попавшуюся
        for y, row in enumerate(self.map_loader.map_data):
            for x, cell in enumerate(row):
                if cell == "L":
                    self.hero.rect.topleft = (x * CELL_SIZE, y * CELL_SIZE)
                    return

    def check_attack_collision(self):
        for monster in self.monsters:
            monster_type = type(monster)
            if not monster.is_dead and self.hero.rect.colliderect(monster.rect):
                if monster not in self.monster_hits[monster_type]["hit_count"]:
                    self.monster_hits[monster_type]["hit_count"][monster] = 0
                self.monster_hits[monster_type]["hit_count"][monster] += 1

                if self.monster_hits[monster_type]["hit_count"][monster] == 1:
                    monster.take_hit()
                elif (self.monster_hits[monster_type]["hit_count"][monster] >=
                      self.monster_hits[monster_type]["hits_to_kill"]):
                    monster.die()

    def check_monster_collision(self):
        current_time = pygame.time.get_ticks()
        for monster in self.monsters:
            if not monster.is_dead and self.hero.rect.colliderect(monster.rect):
                if current_time - self.last_hit_time > self.hit_cooldown:
                    monster.attack()
                    self.lives -= 0.5
                    self.last_hit_time = current_time

                    if self.lives <= 0:
                        self.game_over()

    def draw_health_bar(self):
        """Отображает шкалу жизней в правом верхнем углу."""
        bar_width = 510
        bar_height = 40
        bar_x = self.screen_width - bar_width - 20
        bar_y = 20

        pygame.draw.rect(self.screen, (230, 199, 172), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, (111, 83, 6), (bar_x, bar_y, bar_width, bar_height), 3)

        full_hearts = int(self.lives)
        has_half_heart = self.lives - full_hearts >= 0.5

        for i in range(full_hearts):
            x = bar_x + 10 + (i * 50)
            y = bar_y + 5
            self.screen.blit(self.heart_image, (x, y))

        if has_half_heart:
            x = bar_x + 10 + (full_hearts * 50)
            y = bar_y + 5
            half_heart = self.heart_image.subsurface(0, 0, 15, 30)  # Половина сердца
            self.screen.blit(half_heart, (x, y))

    def game_over(self):
        """Запускает экран окончания игры."""
        game_over_screen = GameOverScreen()
        choice = game_over_screen.run()

        if choice == "NO":
            pygame.quit()
            sys.exit()
        else:
            self.__init__()

    def spawn_monster(self):
        """Спавнит 2-3 монстра сразу, с одинаковым X, но разным Y"""
        num_monsters = random.randint(2, 5)
        spawn_x = 170

        used_y_positions = []

        for _ in range(num_monsters):
            monster_type = random.choices(
                [Sceleton, Eye, Goblin, Mushroom],
                weights=[15, 30, 25, 30],  # Вероятность появления разных типов монстров
                k=1
            )[0]

            # Генерируем уникальную y-координату
            available_y_positions = [200, 250, 300, 350, 400]
            available_y_positions = [y for y in available_y_positions if y not in used_y_positions]

            if not available_y_positions:
                break

            spawn_y = random.choice(available_y_positions)

            used_y_positions.append(spawn_y)

            new_monster = monster_type(self.screen_width, self.screen_height, self.map_loader,
                                       speed=random.uniform(1.0, 2.5))
            new_monster.rect.x = spawn_x
            new_monster.rect.y = spawn_y
            self.monsters.append(new_monster)

    def run(self):
        while True:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.hero.attack_r()
                    self.check_attack_collision()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.hero.attack_l()
                    self.check_attack_collision()

            keys = pygame.key.get_pressed()
            self.hero.move(self.map_loader, keys)
            self.hero.animate()

            if current_time - self.last_spawn > self.spawn_time:
                self.spawn_monster()
                self.last_spawn = current_time

            for monster in self.monsters:
                monster.update()

            self.check_monster_collision()

            self.screen.fill((124, 172, 46))

            self.map_loader.draw_map(self.screen)
            self.screen.blit(self.castle, (self.screen_width // 1.19, self.screen_height // 2.5))

            for monster in self.monsters:
                monster.draw(self.screen)

            self.screen.blit(self.hero.image, self.hero.rect)
            self.draw_health_bar()

            pygame.display.flip()
            self.clock.tick(60)


# if __name__ == "__main__":
#     intro = IntroScreen()
#     if intro.run() == "EXIT":
#         pygame.quit()
#         sys.exit()
#
#     while True:
#         game = Game()
#         game.run()
#
#
if __name__ == "__main__":
    # intro = IntroScreen()
    # intro.run()  # Если нажата "PLAY", продолжаем, иначе закрываем игру
    while True:
        game = Game()
        game.run()

        game_over_screen = GameOverScreen()
        choice = game_over_screen.run()

        if choice == "NO":
            break
