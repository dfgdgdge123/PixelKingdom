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
        """ Проверяет, является ли клетка стеной 'S' """
        cell_x, cell_y = x // CELL_SIZE, y // CELL_SIZE
        if 0 <= cell_y < len(self.map_data) and 0 <= cell_x < len(self.map_data[0]):
            return self.map_data[cell_y][cell_x] == "S"
        return False


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

        self.monsters = [
            Sceleton(self.screen_width, self.screen_height, self.map_loader),
            Eye(self.screen_width, self.screen_height, self.map_loader),
            Goblin(self.screen_width, self.screen_height, self.map_loader),
            Mushroom(self.screen_width, self.screen_height, self.map_loader),
        ]

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
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.hero.attack_r()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.hero.attack_l()

            keys = pygame.key.get_pressed()
            self.hero.move(self.map_loader, keys)
            self.hero.animate()

            # ОБНОВЛЕНИЕ МОНСТРОВ
            for monster in self.monsters:
                monster.update()  # Убираем передачу map_loader

            # Рендеринг
            self.screen.fill((124, 172, 46))
            self.map_loader.draw_map(self.screen)
            self.screen.blit(self.castle, (self.screen_width // 1.19, self.screen_height // 2.5))

            # ОТРИСОВКА МОНСТРОВ
            for monster in self.monsters:
                monster.draw(self.screen)

            self.screen.blit(self.hero.image, self.hero.rect)

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
    # intro = IntroScreen()
    # intro.run()
    # end = GameOverScreen()
    # end.run()