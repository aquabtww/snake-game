import sys

import pygame

from settings import BOARD_OFFSET, BOARD_SIZE, CELL_SIZE, FPS
from board import Board
from events import UPDATE_EVENT


class Game:
    """
    Класс, отвечающий за игру.
    """
    pygame.init()

    def __init__(self):
        pygame.display.set_caption("Змейка")

        self.display = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock()

        self.board: Board = Board(self)

    def game_loop(self) -> None:
        self.display = pygame.display.set_mode(
            (BOARD_OFFSET * 2 + BOARD_SIZE[0] * CELL_SIZE,
             BOARD_OFFSET * 2 + BOARD_SIZE[1] * CELL_SIZE))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause()
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

            pygame.display.update()
            self.clock.tick(FPS)

    def pause(self) -> None:
        self.display = pygame.display.set_mode((800, 800))

        self.display.fill((0, 0, 0))

        font_48 = pygame.font.SysFont("bahnschrift", 48)
        pause_text = font_48.render("Пауза", True, (255, 255, 255))

        self.display.blit(pause_text, (10, 100))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.board.snake.last_direction = None
                    self.board.snake.direction = (0, 0)
                    self.game_loop()
                    break

            pygame.display.update()
            self.clock.tick(FPS)

    def main_menu(self):
        ...

    def lose(self) -> None:
        """
        Поражение в игре.
        :return: Ничего
        """
        self.board.reset()
        self.pause()

    def run(self) -> None:
        """
        Запуск игры.
        :return: Ничего
        """
        self.pause()

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
    game.run()
