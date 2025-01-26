import pygame
import sys

pygame.init()

CELL_SIZE = 50

# Загрузка спрайтов
imgSprites_Run_D = pygame.image.load("hero_assets/_Run.png")
imgSprites_Run_A = pygame.image.load("hero_assets/inv_Run.png")
imgSprites_Run_WS = pygame.image.load("hero_assets/_CrouchAll.png")
stand_sprite = pygame.image.load("hero_assets/hero.png")

# Анимация бега (вырезаем кадры)
animRun_D = [imgSprites_Run_D.subsurface(42, 42, 28, 38),
             imgSprites_Run_D.subsurface(163, 42, 28, 38),
             imgSprites_Run_D.subsurface(287, 42, 28, 38),
             imgSprites_Run_D.subsurface(405, 42, 28, 38),
             imgSprites_Run_D.subsurface(523, 42, 28, 38),
             imgSprites_Run_D.subsurface(641, 42, 28, 38),
             imgSprites_Run_D.subsurface(763, 42, 28, 38),
             imgSprites_Run_D.subsurface(885, 42, 28, 38),
             imgSprites_Run_D.subsurface(1006, 42, 28, 38),
             imgSprites_Run_D.subsurface(1123, 42, 28, 38)]

animRun_A = [imgSprites_Run_A.subsurface(1123, 42, 28, 38),
             imgSprites_Run_A.subsurface(1006, 42, 28, 38),
             imgSprites_Run_A.subsurface(885, 42, 28, 38),
             imgSprites_Run_A.subsurface(763, 42, 28, 38),
             imgSprites_Run_A.subsurface(641, 42, 28, 38),
             imgSprites_Run_A.subsurface(523, 42, 28, 38),
             imgSprites_Run_A.subsurface(405, 42, 28, 38),
             imgSprites_Run_A.subsurface(287, 42, 28, 38),
             imgSprites_Run_A.subsurface(163, 42, 28, 38),
             imgSprites_Run_A.subsurface(42, 42, 28, 38)]

animRun_WS = [imgSprites_Run_WS.subsurface(42, 46, 31, 33),
              imgSprites_Run_WS.subsurface(162, 46, 31, 33),
              imgSprites_Run_WS.subsurface(281, 46, 31, 33)]

# Загрузка ассетов карты
ASSETS = {
    "L": pygame.image.load("map_assets/land.jpg"),
    "G": pygame.image.load("map_assets/grass.jpg"),
    "F": pygame.image.load("map_assets/fild.jpg"),
    "C": pygame.image.load("map_assets/castle_floor.jpg"),
    "S": pygame.image.load("map_assets/castle_walls.jpg"),
    "1": pygame.image.load("map_assets/three1.jpg"),
    "2": pygame.image.load("map_assets/three2.jpg"),
    "3": pygame.image.load("map_assets/three3.jpg"),
    "4": pygame.image.load("map_assets/three3.jpg"),
    "5": pygame.image.load("map_assets/flowers.jpg")
}


def load_map(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file]


def draw_map(map_data, screen):
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell in ASSETS:
                screen.blit(ASSETS[cell], (x * CELL_SIZE, y * CELL_SIZE))


def can_move(map_data, x, y, hero_width, hero_height):
    # Проверяет, можно ли двигаться в клетку (x, y), проверяя все углы героя
    rows = len(map_data)
    cols = len(map_data[0])

    corners = [
        (x // CELL_SIZE, y // CELL_SIZE),
        ((x + hero_width) // CELL_SIZE, y // CELL_SIZE),
        (x // CELL_SIZE, (y + hero_height) // CELL_SIZE),
        ((x + hero_width) // CELL_SIZE, (y + hero_height) // CELL_SIZE),
    ]

    # Проверяем, все ли углы находятся в клетках "L"
    for cell_x, cell_y in corners:
        if not (0 <= cell_y < rows and 0 <= cell_x < cols) or map_data[cell_y][cell_x] != "L":
            return False

    return True


def main():
    frame = 0
    map_data = load_map("map.txt")
    screen_width = len(map_data[0]) * CELL_SIZE
    screen_height = len(map_data) * CELL_SIZE

    castle = pygame.image.load('map_assets/castle.png')

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pixel Kingdom")

    # Создаём героя
    hero = pygame.sprite.Sprite()
    hero.image = stand_sprite
    hero.rect = hero.image.get_rect()

    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell == "L":
                hero.rect.topleft = (x * CELL_SIZE, y * CELL_SIZE)
                break
        else:
            continue
        break

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Движение героя
        keys = pygame.key.get_pressed()
        is_running_D = is_running_A = is_running_W = is_running_S = False

        new_x, new_y = hero.rect.x, hero.rect.y

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            new_x -= 3
            is_running_A = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_x += 3
            is_running_D = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_y += 3
            is_running_S = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            new_y -= 3
            is_running_W = True

        # Проверяем, можно ли двигаться
        if can_move(map_data, new_x, hero.rect.y, hero.rect.width, hero.rect.height):
            hero.rect.x = new_x
        if can_move(map_data, hero.rect.x, new_y, hero.rect.width, hero.rect.height):
            hero.rect.y = new_y

        """Анимация бега"""
        if is_running_D:
            frame = (frame + 0.1) % len(animRun_D)
            hero.image = animRun_D[int(frame)]
        elif is_running_A:
            frame = (frame + 0.1) % len(animRun_A)
            hero.image = animRun_A[int(frame)]
        elif is_running_S or is_running_W:
            frame = (frame + 0.1) % len(animRun_WS)
            hero.image = animRun_WS[int(frame)]
        else:
            hero.image = stand_sprite

        # Отрисовка экрана
        screen.fill((124, 172, 46))
        draw_map(map_data, screen)
        screen.blit(castle, (screen_width // 1.19, screen_height // 2.5))
        screen.blit(hero.image, hero.rect)

        clock.tick(60)
        pygame.display.flip()


if __name__ == "__main__":
    main()
