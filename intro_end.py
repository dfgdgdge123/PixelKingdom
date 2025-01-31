import pygame
import sys


class IntroScreen:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 1280, 720
        self.FONT_PATH = None

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Intro to game")

        self.bg_image = pygame.image.load("intro_end/background.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (self.WIDTH, self.HEIGHT))

        self.font = pygame.font.Font(self.FONT_PATH, 80) if self.FONT_PATH else pygame.font.SysFont("impact", 80)
        self.button_font = pygame.font.Font(self.FONT_PATH, 40) if self.FONT_PATH else pygame.font.SysFont("impact", 40)

    def draw_background(self):
        self.screen.blit(self.bg_image, (0, 0))

    def draw_button(self, text, x, y, color):
        button_width, button_height = 180, 60
        button_rect = pygame.Rect(x, y, button_width, button_height)

        pygame.draw.rect(self.screen, color, button_rect, border_radius=20)

        text_surface = self.button_font.render(text, True, 'BLACK')
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect.topleft)

        return button_rect

    def run(self):
        progress = 0
        clock = pygame.time.Clock()
        bar_x, bar_y = self.WIDTH // 4, 400
        bar_width, bar_height = self.WIDTH // 2, 20

        while progress <= 100:
            self.screen.fill('BLACK')
            self.draw_background()

            title_text = self.font.render("WELCOME TO PIXEL KINGDOM!", True, 'WHITE')
            title_rect = title_text.get_rect(center=(self.WIDTH // 2, 320))
            self.screen.blit(title_text, title_rect.topleft)

            pygame.draw.rect(self.screen, 'WHITE', (bar_x, bar_y, bar_width, bar_height), border_radius=10)
            pygame.draw.rect(self.screen, (59, 179, 234),
                             (bar_x, bar_y, bar_width * (progress / 100), bar_height), border_radius=10)

            pygame.display.flip()
            progress += 2
            clock.tick(30)

        menu_button = self.draw_button("STORY", self.WIDTH // 2 - 90, 500, (255, 200, 50))
        play_button = self.draw_button("PLAY", self.WIDTH // 3 - 90, 500, (240, 80, 80))
        exit_button = self.draw_button("EXIT", self.WIDTH * 2 // 3 - 90, 500, (60, 180, 200))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.collidepoint(event.pos):
                        return "PLAY"  # Возвращаем "PLAY" при нажатии на кнопку "PLAY"
                    elif menu_button.collidepoint(event.pos):
                        return "STORY"  # Возвращаем "STORY" при нажатии на кнопку "STORY"
                    elif exit_button.collidepoint(event.pos):
                        return "EXIT"  # Возвращаем "EXIT" при нажатии на кнопку "EXIT"


class GameOverScreen:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("GAME OVER")
        self.screen = pygame.display.set_mode((600, 500))
        self.width, self.height = self.screen.get_size()

        self.font_large = pygame.font.Font(None, 100)
        self.font_medium = pygame.font.Font(None, 60)
        self.font_small = pygame.font.Font(None, 50)

        self.bg_color = (20, 20, 20)
        self.text_color = (255, 255, 255)
        self.red_color = (200, 50, 50)

        button_width, button_height = 150, 70
        button_y = self.height // 2 + 120

        self.buttons = [
            {"rect": pygame.Rect(self.width // 2 - button_width - 20, button_y, button_width, button_height),
             "color": (230, 230, 230), "text": "YES"},
            {"rect": pygame.Rect(self.width // 2 + 20, button_y, button_width, button_height),
             "color": (200, 50, 50), "text": "NO"}
        ]

    def draw(self):
        self.screen.fill(self.bg_color)

        skull = pygame.image.load("intro_end/skelet.png")
        skull = pygame.transform.scale(skull, (200, 200))
        skull_rect = skull.get_rect(center=(self.width // 2, self.height // 4 - 50))
        self.screen.blit(skull, skull_rect)

        game_over_text = self.font_large.render("GAME OVER", True, self.text_color)
        game_over_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 4 + 120))
        self.screen.blit(game_over_text, game_over_rect)

        play_again_text = self.font_medium.render("PLAY AGAIN?", True, self.red_color)
        play_again_rect = play_again_text.get_rect(center=(self.width // 2, self.height // 2 + 70))
        self.screen.blit(play_again_text, play_again_rect)

        for button in self.buttons:
            pygame.draw.rect(self.screen, button["color"], button["rect"], border_radius=10)
            text = self.font_small.render(button["text"], True,
                                          self.red_color if button["color"] == (230, 230, 230) else self.text_color)
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "NO"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button["rect"].collidepoint(event.pos):
                            if button["text"] == "YES":
                                print("Начинаем игру заново!")
                                return "YES"
                            elif button["text"] == "NO":
                                print("Игра завершена.")
                                return "NO"
            pygame.time.delay(100)
        pygame.quit()


class StoryScreen:
    def __init__(self):
        pygame.init()  # Инициализация Pygame
        pygame.font.init()  # Инициализация шрифтов

        self.screen = pygame.display.set_mode((800, 600))
        self.font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 28)
        self.clock = pygame.time.Clock()

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_button(self, text, x, y, width, height, color, hover_color):
        mouse_pos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]

        button_rect = pygame.Rect(x, y, width, height)
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, hover_color, button_rect)
            if clicked:
                return True
        else:
            pygame.draw.rect(self.screen, color, button_rect)

        text_surface = self.button_font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        return False

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Черный фон

            # Отрисовка текста описания
            self.draw_text("Описание игры:", 50, 50)
            self.draw_text("Здесь будет описание игры.", 50, 100)
            self.draw_text("Вы можете добавить сюда любой текст,", 50, 150)
            self.draw_text("который расскажет игроку о сюжете.", 50, 200)

            # Кнопка возврата на интро
            if self.draw_button("Вернуться", 350, 500, 100, 50, (100, 100, 100), (150, 150, 150)):
                running = False  # Закрываем экран StoryScreen и возвращаемся на IntroScreen

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    pygame.init()  # Глобальная инициализация Pygame
    story = StoryScreen()
    story.run()



if __name__ == "__main__":
    # intro = IntroScreen()
    # intro.run()
    story = StoryScreen()
    story.run()
    # game_over_screen = GameOverScreen()
    # game_over_screen.run()

