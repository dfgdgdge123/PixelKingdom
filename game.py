import random

import pygame
import sys
import sqlite3
from intro_end import IntroScreen, GameOverScreen, StatsScreen, WinScreen
from monsters import Sceleton, Eye, Goblin, Mushroom
from hero import Hero
from map_loader import MapLoader

pygame.init()

CELL_SIZE = 50


class Game:
    def __init__(self, level=1):
        pygame.init()
        self.level = level
        self.map_loader = MapLoader(f"map_level{level}.txt", self.level)  # Загружаем карту в зависимости от уровня
        self.screen_width = len(self.map_loader.map_data[0]) * CELL_SIZE
        self.screen_height = len(self.map_loader.map_data) * CELL_SIZE
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(f"Pixel Kingdom - Level {level}")

        self.heart_image = pygame.image.load("hero_assets/heart.png")
        self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))

        self.start_time = pygame.time.get_ticks()
        self.is_game_over = False
        self.damage_taken = 0

        self.castle = pygame.image.load('map_assets/castle.png')
        self.background_color = (124, 172, 46) if level == 1 else (244, 225, 173)
        self.hero = Hero()
        self.clock = pygame.time.Clock()
        self.init_hero_position()

        self.sceleton_hp = 5
        self.eye_hp = 3
        self.goblin_hp = 2
        self.mushroom_hp = 4
        if level == 2:  # увеличение хп монстров на 2-м уровне
            self.sceleton_hp = self.sceleton_hp * 1.5
            self.eye_hp = self.eye_hp * 1.5
            self.goblin_hp = self.goblin_hp * 1.5
            self.mushroom_hp = self.mushroom_hp * 1.5
        self.monster_hits = {
            Sceleton: {"hits_to_kill": self.sceleton_hp, "hit_count": {}},
            Eye: {"hits_to_kill": self.eye_hp, "hit_count": {}},
            Goblin: {"hits_to_kill": self.goblin_hp, "hit_count": {}},
            Mushroom: {"hits_to_kill": self.mushroom_hp, "hit_count": {}},
        }

        self.last_hit_time = 0
        self.hit_cooldown = 1500

        self.monsters = []
        self.spawn_time = 5000  # Интервал спавна в миллисекундах (5 секунд)
        self.last_spawn = pygame.time.get_ticks()

        self.bonuses = []
        self.monsters_killed = 0

        # Камера
        self.camera_x = 0
        self.camera_y = 0
        self.camera_zoom = 1.2  # Увеличение камеры
        self.camera_smoothness = 0.1  # Плавность движения камеры

        self.chest_closed_image = pygame.image.load("map_assets/chest.png").subsurface(255, 133, 211, 163)
        self.chest_opened_image = pygame.image.load("map_assets/chest.png").subsurface(40, 70, 218, 232)
        self.chest_rect = pygame.Rect(self.screen_width // 1.19 + 50, self.screen_height // 2.5 + 100, 50, 50)
        self.chest_opened = False  # Флаг, открыт ли сундук

    def apply_camera(self, surface, rect):
        """Применяет смещение и масштабирование камеры к объекту."""
        scaled_rect = pygame.Rect(
            (rect.x - self.camera_x) * self.camera_zoom,
            (rect.y - self.camera_y) * self.camera_zoom,
            rect.width * self.camera_zoom,
            rect.height * self.camera_zoom
        )
        scaled_surface = pygame.transform.scale(surface, (scaled_rect.width, scaled_rect.height))
        return scaled_surface, scaled_rect

    def update_camera(self):
        """Обновляет позицию камеры, чтобы следовать за героем."""
        target_x = self.hero.rect.x - self.screen_width // (2 * self.camera_zoom)
        target_y = self.hero.rect.y - self.screen_height // (2 * self.camera_zoom)

        # Движение камеры
        self.camera_x += (target_x - self.camera_x) * self.camera_smoothness
        self.camera_y += (target_y - self.camera_y) * self.camera_smoothness

    def init_hero_position(self):
        # Находим середину карты
        mid_y = len(self.map_loader.map_data) // 2
        mid_x = len(self.map_loader.map_data[0]) // 2

        for y in range(mid_y - 1, mid_y + 2):
            for x in range(mid_x - 1, mid_x + 2):
                if 0 <= y < len(self.map_loader.map_data) and 0 <= x < len(self.map_loader.map_data[0]):
                    if self.map_loader.map_data[y][x] == "L":
                        self.hero.rect.topleft = (x * CELL_SIZE, y * CELL_SIZE)
                        return

        for y, row in enumerate(self.map_loader.map_data):
            for x, cell in enumerate(row):
                if cell == "L":
                    self.hero.rect.topleft = (x * CELL_SIZE, y * CELL_SIZE)
                    return

    def check_effects(self):
        if self.hero.speed > 3:
            this_time = pygame.time.get_ticks()
            if this_time - self.hero.speed_effect_time >= 5000:
                self.hero.speed = 3
                self.hero.speed_effect_time = None
        if self.hero.attack_power > 1:
            this_time = pygame.time.get_ticks()
            if this_time - self.hero.attack_effect_time >= 5000:
                self.hero.attack_power = 1
                self.hero.attack_effect_time = None

    def check_attack_collision(self):
        """Обрабатывает атаку героя и убийство монстров."""
        pygame.time.get_ticks()
        self.hero.attack_area.center = self.hero.rect.center
        for monster in self.monsters[:]:  # Копируем список, чтобы безопасно удалять элементы
            monster_type = type(monster)
            if not monster.is_dead and self.hero.attack_area.colliderect(monster.rect):
                if monster not in self.monster_hits[monster_type]["hit_count"]:
                    self.monster_hits[monster_type]["hit_count"][monster] = 0
                self.monster_hits[monster_type]["hit_count"][monster] += self.hero.attack_power

                if (1 <= self.monster_hits[monster_type]["hit_count"][monster] <=
                        self.monster_hits[monster_type]["hits_to_kill"]):
                    monster.take_hit()
                if (self.monster_hits[monster_type]["hit_count"][monster] >=
                        self.monster_hits[monster_type]["hits_to_kill"]):
                    self.monsters_killed += 1  # Увеличиваем счётчик убитых монстров
                    monster.die()
                    # self.monsters.remove(monster)  # Удаляем монстра из списка
                    # self.check_victory_conditions()  # Проверяем победу

    def check_monster_collision(self):
        current_time = pygame.time.get_ticks()
        for monster in self.monsters:
            if not monster.is_dead and self.hero.rect.colliderect(monster.rect):
                if current_time - self.last_hit_time > self.hit_cooldown:
                    monster.attack()
                    self.last_hit_time = current_time

                    self.damage_taken += 1

    def draw_health_bar(self):
        """Отображает шкалу жизней в правом верхнем углу."""
        bar_width = 250
        bar_height = 40
        bar_x = self.screen_width - bar_width - 20
        bar_y = 20

        pygame.draw.rect(self.screen, (230, 199, 172), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, (111, 83, 6), (bar_x, bar_y, bar_width, bar_height), 3)

        full_hearts = int(self.hero.lives)
        has_half_heart = self.hero.lives - full_hearts >= 0.5

        for i in range(full_hearts):
            x = bar_x + 10 + (i * 50)
            y = bar_y + 5
            self.screen.blit(self.heart_image, (x, y))

        if has_half_heart:
            x = bar_x + 10 + (full_hearts * 50)
            y = bar_y + 5
            half_heart = self.heart_image.subsurface(0, 0, 15, 30)  # Половина сердца
            self.screen.blit(half_heart, (x, y))

    def draw_kill_counter(self):
        """Отображает количество убитых монстров в левом верхнем углу."""
        font = pygame.font.Font(None, 36)
        text = font.render(f"Убито монстров: {self.monsters_killed}", True, (255, 255, 255))

        # Фон под текстом
        text_bg_rect = pygame.Rect(15, 15, 250, 32)
        pygame.draw.rect(self.screen, (0, 0, 0, 128), text_bg_rect)

        self.screen.blit(text, (20, 20))

    def game_over(self, reason):
        """Запускает экран окончания игры и сохраняет результаты."""
        self.save_game_over_results(reason)
        self.is_game_over = True

        game_over_screen = GameOverScreen()
        choice, level = game_over_screen.run(self.level)  # Передаем текущий уровень в GameOverScreen

        if choice == "NO":
            pygame.quit()
            sys.exit()
        else:
            # Перезапускаем игру с текущим уровнем
            game = Game(level=level)
            game.run()

    def spawn_monster(self):
        """Спавнит 2-3 монстра сразу, с одинаковым X, но разным Y"""
        num_monsters = random.randint(2, 5)
        spawn_x = 170

        used_y_positions = []

        for _ in range(num_monsters):
            monster_type = random.choices(
                [Sceleton, Eye, Goblin, Mushroom],
                weights=[20, 30, 25, 30],  # Вероятность появления разных типов монстров
                k=1
            )[0]

            available_y_positions = [200, 250, 300, 350, 400]
            available_y_positions = [y for y in available_y_positions if y not in used_y_positions]

            if not available_y_positions:
                break

            spawn_y = random.choice(available_y_positions)

            used_y_positions.append(spawn_y)

            new_monster = monster_type(self.screen_width, self.screen_height, self.map_loader,
                                       speed=random.uniform(1.0, 2.5), game=self)

            new_monster.rect.x = spawn_x
            new_monster.rect.y = spawn_y
            self.monsters.append(new_monster)

    def check_bonus_collision(self):
        """Проверяет, взял ли герой бонус, и применяет эффект."""
        for bonus in self.bonuses[:]:
            if self.hero.rect.colliderect(bonus.rect):
                bonus.apply(self.hero)
                self.bonuses.remove(bonus)

    def animate_camera_to_castle(self):
        """Анимация приближения камеры к замку."""
        target_x = self.screen_width // 1 - self.screen_width // (2 * self.camera_zoom)
        target_y = self.screen_height // 1.5 - self.screen_height // (2 * self.camera_zoom)

        # движение камеры к замку
        while abs(self.camera_x - target_x) > 1 or abs(self.camera_y - target_y) > 1:
            self.camera_x += (target_x - self.camera_x) * 0.1
            self.camera_y += (target_y - self.camera_y) * 0.1
            self.camera_zoom += 0.01

            self.screen.fill((124, 172, 46))
            self.map_loader.draw_map(self.screen, self.camera_x, self.camera_y, self.camera_zoom)

            castle_surface, castle_rect = self.apply_camera(self.castle, self.castle.get_rect(
                topleft=(self.screen_width // 1.19, self.screen_height // 2.5)))
            self.screen.blit(castle_surface, castle_rect)

            pygame.display.flip()
            self.clock.tick(60)

    def win_game(self):
        """Анимация приближения, ожидание клика по сундуку, затем запуск экрана победы."""
        self.animate_camera_to_castle()
        self.save_results(self.level)

        self.chest_opened = False
        self.chest_image = self.chest_closed_image

        waiting_for_click = True
        while waiting_for_click:
            self.screen.fill((124, 172, 46))
            self.map_loader.draw_map(self.screen, self.camera_x, self.camera_y, self.camera_zoom)

            castle_surface, castle_rect = self.apply_camera(self.castle, self.castle.get_rect(
                topleft=(self.screen_width // 1.19, self.screen_height // 2.5)))
            self.screen.blit(castle_surface, castle_rect)

            chest_surface, chest_rect = self.apply_camera(self.chest_image, self.chest_rect)
            self.screen.blit(chest_surface, chest_rect)

            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if chest_rect.collidepoint(event.pos):
                        self.chest_opened = True
                        self.chest_image = self.chest_opened_image
                        waiting_for_click = False

                        chest_surface, chest_rect = self.apply_camera(self.chest_image, self.chest_rect)
                        self.screen.blit(chest_surface, chest_rect)
                        pygame.display.flip()
                        pygame.time.delay(5000)

                        win_screen = WinScreen()
                        choice, level = win_screen.run(self.level)

                        if choice == "RESTART":
                            game = Game(level=1)
                            game.run()
                        elif choice == "NEXT":
                            game = Game(level=2)
                            game.run()
                        elif choice == "EXIT":
                            pygame.quit()
                            sys.exit()

    def save_results(self, level):
        """Сохраняет результаты игры в базу данных."""
        total_time = pygame.time.get_ticks() - self.start_time
        con = sqlite3.connect("results.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM results""").fetchall()
        games, kills, wins, defeats, time_in_game, deaths, castle_destructions, levels_passed = result[0]
        levels_passed += 1
        kills += self.monsters_killed
        if level == 2:
            wins += 1
        time_in_game += total_time // 1000  # время, проведенное в игре в секундах
        cur.execute(
            '''UPDATE results SET games = ?, kills = ?, time_in_game = ?,
             levels_passed = ?, wins = ?''',
            (games, kills, time_in_game, levels_passed, wins))
        con.commit()
        con.close()

    def save_game_over_results(self, reason):
        """Сохраняет результаты игры при проигрыше."""
        total_time = pygame.time.get_ticks() - self.start_time
        con = sqlite3.connect("results.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM results""").fetchall()
        games, kills, wins, defeats, time_in_game, deaths, castle_destructions, levels_passed = result[0]
        games += 1
        kills += self.monsters_killed
        defeats += 1
        if reason == 'castle_death':
            castle_destructions += 1
        elif reason == 'death':
            deaths += 1
        time_in_game += total_time // 1000  # время, проведенное в игре в секундах
        cur.execute(
            '''UPDATE results SET games = ?, kills = ?, defeats = ?, time_in_game = ?,
             deaths = ?, castle_destructions = ?''',
            (games, kills, defeats, time_in_game, deaths, castle_destructions))
        con.commit()
        con.close()

    def save_results_after_exit(self):
        """Сохраняет результаты при выходе из игры."""
        if not self.is_game_over:
            total_time = pygame.time.get_ticks() - self.start_time
            con = sqlite3.connect("results.db")
            cur = con.cursor()
            result = cur.execute("""SELECT * FROM results""").fetchall()
            games, kills, wins, defeats, time_in_game, deaths, castle_destructions, levels_passed = result[0]
            games += 1
            kills += self.monsters_killed
            time_in_game += total_time // 1000  # время, проведенное в игре в секундах
            cur.execute(
                '''UPDATE results SET games = ?, kills = ?, time_in_game = ?''',
                (games, kills, time_in_game))
            con.commit()
            con.close()

    def run(self):
        while True:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_results_after_exit()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and (event.button == 3 or event.button == 1) and not (
                        self.hero.is_r_attacking or self.hero.is_l_attacking):
                    if self.hero.last_horizontal_direction == 'right':
                        self.hero.attack_r()
                    elif self.hero.last_horizontal_direction == 'left':
                        self.hero.attack_l()
                    self.check_attack_collision()

            keys = pygame.key.get_pressed()
            self.hero.move(self.map_loader, keys)
            self.hero.animate()

            if current_time - self.last_spawn > self.spawn_time:
                self.spawn_monster()
                self.last_spawn = current_time

            for monster in self.monsters:
                monster.update(self, self.hero)

                # Проверяем, достиг ли монстр стены замка
                if monster.reached_castle:
                    self.game_over("castle_death")
                    return  # Завершаем игру

            self.check_monster_collision()
            self.check_bonus_collision()

            # Проверка условий выигрыша
            if self.monsters_killed >= 15 and self.hero.lives > 0:
                self.win_game()

            self.screen.fill(self.background_color)

            self.update_camera()

            self.map_loader.draw_map(self.screen, self.camera_x, self.camera_y, self.camera_zoom)

            castle_surface, castle_rect = self.apply_camera(self.castle, self.castle.get_rect(
                topleft=(self.screen_width // 1.19, self.screen_height // 2.5)))
            self.screen.blit(castle_surface, castle_rect)

            for monster in self.monsters:
                monster_surface, monster_rect = self.apply_camera(monster.image, monster.rect)
                self.screen.blit(monster_surface, monster_rect)

            for bonus in self.bonuses:
                bonus_surface, bonus_rect = self.apply_camera(bonus.image, bonus.rect)
                self.screen.blit(bonus_surface, bonus_rect)

            hero_surface, hero_rect = self.apply_camera(self.hero.image, self.hero.rect_for_anim)
            self.screen.blit(hero_surface, hero_rect)

            self.draw_health_bar()
            self.draw_kill_counter()
            self.check_effects()
            self.hero.attack_area.center = self.hero.rect.center
            self.hero.rect_for_anim.center = self.hero.rect.center

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    while True:

        intro = IntroScreen()
        choice = intro.run()

        if choice == "PLAY":
            while True:
                game = Game(level=1)  # Запуск первого уровня
                game.run()

                game_over_screen = GameOverScreen()
                choice = game_over_screen.run(game.level)

                if choice == "NO":
                    break

        elif choice == "STATS":
            stats_screen = StatsScreen()
            stats_screen.run()

        elif choice == "EXIT":
            pygame.quit()
            sys.exit()
