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

        self.heart_image = pygame.image.load("hero_assets/heart.png")  # Укажите путь к файлу сердца
        self.heart_image = pygame.transform.scale(self.heart_image, (40, 40))  # Масштабируем

        self.lives = 3  # Количество жизней героя

        self.castle = pygame.image.load('map_assets/castle.png')
        self.hero = Hero()
        self.clock = pygame.time.Clock()
        self.init_hero_position()

        self.monsters = [
            Sceleton(self.screen_width, self.screen_height, self.map_loader, speed=1),
            Eye(self.screen_width, self.screen_height, self.map_loader, speed=1.5),
            Goblin(self.screen_width, self.screen_height, self.map_loader, speed=2),
            Mushroom(self.screen_width, self.screen_height, self.map_loader, speed=1.3),
        ]

        self.hits_to_kill_sceleton = 2  # Количество ударов для убийства скелета
        self.sceleton_hit_count = {}  # Счетчик ударов по каждому скелету
        self.last_hit_time = 0  # Время последнего удара по герою
        self.hit_cooldown = 1000  # Кулдаун между ударами (в миллисекундах)

        self.hits_to_kill_eye = 2  # Количество ударов для убийства скелета
        self.eye_hit_count = {}

        self.hits_to_kill_goblin = 2  # Количество ударов для убийства скелета
        self.goblin_hit_count = {}

        self.hits_to_kill_mushroom = 2  # Количество ударов для убийства скелета
        self.mushroom_hit_count = {}

    def init_hero_position(self):
        for y, row in enumerate(self.map_loader.map_data):
            for x, cell in enumerate(row):
                if cell == "L":
                    self.hero.rect.topleft = (x * CELL_SIZE, y * CELL_SIZE)
                    return

    def check_attack_collision(self):
        for monster in self.monsters:
            if isinstance(monster, Sceleton) and not monster.is_dead:
                if self.hero.rect.colliderect(monster.rect):
                    if monster not in self.sceleton_hit_count:
                        self.sceleton_hit_count[monster] = 0
                    self.sceleton_hit_count[monster] += 1

                    if self.sceleton_hit_count[monster] == 1:
                        monster.take_hit()  # Запускаем анимацию получения урона
                    elif self.sceleton_hit_count[monster] >= self.hits_to_kill_sceleton:
                        monster.die()  # Запускаем анимацию смерти
            if isinstance(monster, Eye) and not monster.is_dead:
                if self.hero.rect.colliderect(monster.rect):
                    if monster not in self.eye_hit_count:
                        self.eye_hit_count[monster] = 0
                    self.eye_hit_count[monster] += 1

                    if self.eye_hit_count[monster] == 1:
                        monster.take_hit()  # Запускаем анимацию получения уронаa
                    elif self.eye_hit_count[monster] >= self.hits_to_kill_eye:
                        monster.die()  # Запускаем анимацию смерти
            if isinstance(monster, Goblin) and not monster.is_dead:
                if self.hero.rect.colliderect(monster.rect):
                    if monster not in self.goblin_hit_count:
                        self.goblin_hit_count[monster] = 0
                    self.goblin_hit_count[monster] += 1

                    if self.goblin_hit_count[monster] == 1:
                        monster.take_hit()  # Запускаем анимацию получения уронаa
                    elif self.goblin_hit_count[monster] >= self.hits_to_kill_goblin:
                        monster.die()  # Запускаем анимацию смерти
            if isinstance(monster, Mushroom) and not monster.is_dead:
                if self.hero.rect.colliderect(monster.rect):
                    if monster not in self.mushroom_hit_count:
                        self.mushroom_hit_count[monster] = 0
                    self.mushroom_hit_count[monster] += 1

                    if self.mushroom_hit_count[monster] == 1:
                        monster.take_hit()  # Запускаем анимацию получения уронаa
                    elif self.mushroom_hit_count[monster] >= self.hits_to_kill_mushroom:
                        monster.die()  # Запускаем анимацию смерти

    def check_monster_collision(self):
        current_time = pygame.time.get_ticks()
        for monster in self.monsters:
            if isinstance(monster, Sceleton) and not monster.is_dead:
                if self.hero.rect.colliderect(monster.rect):
                    if current_time - self.last_hit_time > self.hit_cooldown:
                        monster.attack()  # Запускаем анимацию атаки скелета
                        self.lives -= 1  # Уменьшаем жизни героя
                        self.last_hit_time = current_time  # Обновляем время последнего удара
            if isinstance(monster, Eye) and not monster.is_dead:
                if self.hero.rect.colliderect(monster.rect):
                    if current_time - self.last_hit_time > self.hit_cooldown:
                        monster.attack()  # Запускаем анимацию атаки скелета
                        self.lives -= 1  # Уменьшаем жизни героя
                        self.last_hit_time = current_time  # Обновляем время последнего удара
            if isinstance(monster, Goblin) and not monster.is_dead:
                if self.hero.rect.colliderect(monster.rect):
                    if current_time - self.last_hit_time > self.hit_cooldown:
                        monster.attack()  # Запускаем анимацию атаки скелета
                        self.lives -= 1  # Уменьшаем жизни героя
                        self.last_hit_time = current_time  # Обновляем время последнего удара
            if isinstance(monster, Mushroom) and not monster.is_dead:
                if self.hero.rect.colliderect(monster.rect):
                    if current_time - self.last_hit_time > self.hit_cooldown:
                        monster.attack()  # Запускаем анимацию атаки скелета
                        self.lives -= 1  # Уменьшаем жизни героя
                        self.last_hit_time = current_time  # Обновляем время последнего удара


    def draw_health_bar(self):
        """Отображает шкалу жизней в правом верхнем углу на белом фоне с чёрной рамкой."""
        bar_width = 160  # Ширина фона под жизни
        bar_height = 50  # Высота фона
        bar_x = self.screen_width - bar_width - 20  # Координаты фона (отступ 20px от края)
        bar_y = 20

        # Рисуем белый прямоугольник
        pygame.draw.rect(self.screen, (230, 199, 172), (bar_x, bar_y, bar_width, bar_height))

        # Рисуем чёрную рамку вокруг
        pygame.draw.rect(self.screen, (111, 83, 6), (bar_x, bar_y, bar_width, bar_height), 3)

        # Отрисовываем сердца
        for i in range(self.lives):
            x = bar_x + 10 + (i * 50)  # Отступ от левого края белого прямоугольника
            y = bar_y + 5  # Отступ сверху внутри белого фона
            self.screen.blit(self.heart_image, (x, y))

    def run(self):
        while True:
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

            # ОБНОВЛЕНИЕ МОНСТРОВ
            for monster in self.monsters:
                monster.update()

            # Проверка столкновений с героем
            self.check_monster_collision()

            # Рендеринг
            self.screen.fill((124, 172, 46))
            self.map_loader.draw_map(self.screen)
            self.screen.blit(self.castle, (self.screen_width // 1.19, self.screen_height // 2.5))

            # ОТРИСОВКА МОНСТРОВ
            for monster in self.monsters:
                monster.draw(self.screen)

            self.screen.blit(self.hero.image, self.hero.rect)

            self.draw_health_bar()

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
    # intro = IntroScreen()
    # intro.run()
    # end = GameOverScreen()
    # end.run()