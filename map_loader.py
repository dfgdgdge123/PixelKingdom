import pygame

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
