import pygame
import gif_pygame
import sys

pygame.init()

CELL_SIZE = 50

ASSETS = {
    "L": pygame.image.load("map_assets/land.jpg"),
    "G": pygame.image.load("map_assets/grass.jpg"),
    "F": pygame.image.load("map_assets/fild.jpg"),
    "C": pygame.image.load("map_assets/castle_floor.jpg"),
    "S": pygame.image.load("map_assets/castle_walls.jpg"),
}

# герой
gif_sprite = gif_pygame.load("hero_assets/knight.gif")


def load_map(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file]


def draw_map(map_data, screen):
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell in ASSETS:
                screen.blit(ASSETS[cell], (x * CELL_SIZE, y * CELL_SIZE))


def main():
    map_data = load_map("map.txt")
    screen_width = len(map_data[0]) * CELL_SIZE
    screen_height = len(map_data) * CELL_SIZE

    castle = pygame.image.load('map_assets/castle.png')  # замок

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pixel Kingdom")

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((124, 172, 46))
        draw_map(map_data, screen)

        gif_sprite.render(screen, gif_sprite.get_rect(center=(screen_width // 2, screen_height // 2)))
        screen.blit(castle, (screen_width // 1.19, screen_height // 2.5))

        clock.tick(60)
        pygame.display.flip()


if __name__ == "__main__":
    main()