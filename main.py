import sys

import pygame

import settings
from board import Board
from events import UPDATE_EVENT
from ui import Button


class Game:
    """
    Класс, отвечающий за игру.
    """
    pygame.init()

    font_30 = pygame.font.SysFont("bahnschrift", 30)
    font_48 = pygame.font.SysFont("bahnschrift", 48)

    def __init__(self):
        pygame.display.set_caption("Змейка")

        self.display = pygame.display.set_mode((400, 400))
        self.clock = pygame.time.Clock()

        self.board: Board = Board(self)

    def game_loop(self) -> None:
        offset = settings.BOARD_OFFSET
        width, height = settings.BOARD_SIZE
        cell_size = settings.CELL_SIZE

        self.display = pygame.display.set_mode(
            (offset * 2 + width * cell_size,
             offset * 2 + height * cell_size))

        pygame.time.set_timer(UPDATE_EVENT, settings.UPDATE_SPEED)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_game()
                        break

                    directions = {
                        pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1),
                        pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0)
                    }
                    if event.key in directions:
                        self.board.snake.set_direction(directions[event.key])

                if event.type == UPDATE_EVENT:
                    self.board.update()

                    self.board.render(self.display)
                    self.board.snake.render(self.display)
                    for apple in self.board.apples:
                        apple.render(self.display)
                    for wall in self.board.walls:
                        wall.render(self.display)

                    score = Game.font_30.render(str(len(self.board.snake.positions) - 1), True, (255, 255, 255))
                    self.display.blit(score, (offset + width * cell_size // 2, 20))

            pygame.display.update()
            self.clock.tick(settings.FPS)

    def pause_game(self) -> None:
        self.display = pygame.display.set_mode((650, 300))

        pause_text = Game.font_48.render("Пауза", True, (255, 255, 255))

        buttons = [
            Button(rect=pygame.rect.Rect(20, 100, 250, 40),
                   text="Продолжить", font=Game.font_30, callback=self.continue_game),
            Button(rect=pygame.rect.Rect(20, 150, 250, 40),
                   text="Главное меню", font=Game.font_30, callback=self.main_menu)
        ]

        while True:
            self.display.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    for button in buttons:
                        button.check_input()

            for button in buttons:
                button.render(self.display)

            self.display.blit(pause_text, (20, 40))

            pygame.display.update()
            self.clock.tick(settings.FPS)

    def continue_game(self):
        self.board.snake.last_direction = None
        self.board.snake.direction = (0, 0)
        self.game_loop()

    def main_menu(self):
        self.display = pygame.display.set_mode((400, 400))

        buttons = [
            Button(rect=pygame.rect.Rect(20, 20, 200, 40),
                   text="Играть", font=Game.font_30, callback=lambda: (self.board.reset(), self.game_loop())),
            Button(rect=pygame.rect.Rect(20, 75, 200, 40),
                   text="Настройки", font=Game.font_30, callback=self.settings_menu)
        ]

        while True:
            self.display.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    for button in buttons:
                        button.check_input()

            for button in buttons:
                button.render(self.display)

            pygame.display.update()
            self.clock.tick(settings.FPS)

    def settings_menu(self):
        self.display = pygame.display.set_mode((485, 500))

        buttons = [
            Button(rect=pygame.rect.Rect(20, 20, 250, 40),
                   text="Главное меню", font=Game.font_30, callback=self.main_menu),

            Button(rect=pygame.rect.Rect(75, 75, 340, 40),
                   text=f"Скорость Игры ({settings.UPDATE_SPEED}мс)", font=Game.font_30),
            Button(rect=pygame.rect.Rect(20, 75, 40, 40),
                   text="-", font=Game.font_30, callback=settings.take_speed),
            Button(rect=pygame.rect.Rect(430, 75, 40, 40),
                   text="+", font=Game.font_30, callback=settings.add_speed),

            Button(rect=pygame.rect.Rect(75, 130, 340, 40),
                   text=f"Ширина поля ({settings.BOARD_SIZE[0]})", font=Game.font_30),
            Button(rect=pygame.rect.Rect(20, 130, 40, 40),
                   text="-", font=Game.font_30, callback=settings.take_width),
            Button(rect=pygame.rect.Rect(430, 130, 40, 40),
                   text="+", font=Game.font_30, callback=settings.add_width),

            Button(rect=pygame.rect.Rect(75, 185, 340, 40),
                   text=f"Высота поля ({settings.BOARD_SIZE[1]})", font=Game.font_30),
            Button(rect=pygame.rect.Rect(20, 185, 40, 40),
                   text="-", font=Game.font_30, callback=settings.take_height),
            Button(rect=pygame.rect.Rect(430, 185, 40, 40),
                   text="+", font=Game.font_30, callback=settings.add_height),

            Button(rect=pygame.rect.Rect(75, 240, 340, 40),
                   text=f"Количество стен ({settings.WALL_AMOUNT})", font=Game.font_30),
            Button(rect=pygame.rect.Rect(20, 240, 40, 40),
                   text="-", font=Game.font_30, callback=settings.take_wall),
            Button(rect=pygame.rect.Rect(430, 240, 40, 40),
                   text="+", font=Game.font_30, callback=settings.add_wall),

            Button(rect=pygame.rect.Rect(75, 295, 340, 40),
                   text=f"Количество яблок ({settings.APPLE_AMOUNT})", font=Game.font_30),
            Button(rect=pygame.rect.Rect(20, 295, 40, 40),
                   text="-", font=Game.font_30, callback=settings.take_apple),
            Button(rect=pygame.rect.Rect(430, 295, 40, 40),
                   text="+", font=Game.font_30, callback=settings.add_apple)
        ]

        while True:
            self.display.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    for button in buttons:
                        button.check_input()

            buttons[1].update_text(f"Скорость Игры ({settings.UPDATE_SPEED}мс)")
            buttons[4].update_text(f"Ширина поля ({settings.BOARD_SIZE[0]})")
            buttons[7].update_text(f"Высота поля ({settings.BOARD_SIZE[1]})")
            buttons[10].update_text(f"Количество стен ({settings.WALL_AMOUNT})")
            buttons[13].update_text(f"Количество яблок ({settings.APPLE_AMOUNT})")

            for button in buttons:
                button.render(self.display)

            pygame.display.update()
            self.clock.tick(settings.FPS)

    def end_screen(self, msg: str):
        self.display = pygame.display.set_mode((400, 400))

        win_text = Game.font_48.render(msg, True, (255, 255, 255))
        score_text = Game.font_30.render(f"Счет: {len(self.board.snake.positions) - 1}", True, (255, 255, 255))

        buttons = [
            Button(rect=pygame.rect.Rect(25, 120, 240, 40),
                   text="Играть", font=Game.font_30, callback=lambda: (self.board.reset(), self.game_loop())),
            Button(rect=pygame.rect.Rect(25, 175, 240, 40),
                   text="Главное меню", font=Game.font_30, callback=self.main_menu)
        ]

        while True:
            self.display.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    for button in buttons:
                        button.check_input()

            self.display.blit(win_text, (20, 40))
            self.display.blit(score_text, (20, 85))

            for button in buttons:
                button.render(self.display)

            pygame.display.update()
            self.clock.tick(settings.FPS)

    def win_screen(self):
        """
        Экран победы.
        :return: Ничего
        """
        self.end_screen("Победа!")

    def lose_screen(self):
        """
        Экран поражения.
        :return: Ничего
        """
        self.end_screen("Поражение!")

    def lose(self) -> None:
        """
        Поражение в игре.
        :return: Ничего
        """
        self.lose_screen()

    def win(self) -> None:
        """
        Победа в игре.
        :return: Ничего
        """
        self.win_screen()

    @staticmethod
    def quit() -> None:
        """
        Закрытие игры.
        :return: Ничего
        """
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.main_menu()
