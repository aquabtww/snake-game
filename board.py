import pygame
from pygame import Surface

from events import UPDATE_EVENT
from settings import BOARD_SIZE, CELL_SIZE, BOARD_OFFSET, UPDATE_SPEED
from utils import get_cell_rect, lerp, random_coordinates


class Board:
    def __init__(self, game):
        self.game = game

        pygame.time.set_timer(UPDATE_EVENT, UPDATE_SPEED)

        self.snake = Snake(game)
        self.snake.positions.append((2, 2))

        self.apples: list[Apple] = []
        self.spawn_apple()

    def reset(self):
        self.snake.reset()
        self.snake.positions.append((2, 2))

        self.apples: list[Apple] = []
        self.spawn_apple()

    def spawn_apple(self):
        apple_pos = random_coordinates()
        check = False
        while not check:
            if apple_pos in self.snake.positions:
                apple_pos = random_coordinates()
                continue
            check = True
        apple = Apple(*apple_pos)
        self.apples.append(apple)

    def update(self):
        self.snake.move()

    @staticmethod
    def render(display):
        display.fill((0, 0, 0))
        width, height = BOARD_SIZE
        for x in range(width + 1):
            pygame.draw.line(display, (255, 255, 255),
                             (BOARD_OFFSET + x * CELL_SIZE, BOARD_OFFSET),
                             (BOARD_OFFSET + x * CELL_SIZE, BOARD_OFFSET + height * CELL_SIZE))
        for y in range(height + 1):
            pygame.draw.line(display, (255, 255, 255),
                             (BOARD_OFFSET, BOARD_OFFSET + y * CELL_SIZE),
                             (BOARD_OFFSET + width * CELL_SIZE, BOARD_OFFSET + y * CELL_SIZE))


class Snake:
    def __init__(self, game):
        self.game = game

        self.last_direction = None
        self.direction = (0, 0)
        self.positions = []

    def reset(self) -> None:
        self.last_direction = None
        self.direction = (0, 0)
        self.positions = []

    def set_direction(self, direction: tuple[int, int]) -> None:
        x, y = direction
        if self.last_direction is not None and sum(self.last_direction) != 0:
            if self.last_direction[0] == x * -1 or self.last_direction[1] == y * -1:
                return
        self.direction = (x, y)

    def move(self) -> None:
        if self.direction == (0, 0):
            return

        new_head_position = self.positions[-1][0] + self.direction[0], self.positions[-1][1] + self.direction[1]
        if (new_head_position[0] < 0 or new_head_position[0] >= BOARD_SIZE[0]) or \
                (new_head_position[1] < 0 or new_head_position[1] >= BOARD_SIZE[1]) or \
                new_head_position in self.positions[1:]:
            self.game.lose()

        self.last_direction = self.direction
        for apple in self.game.board.apples:
            if apple.check_eat(new_head_position):
                self.positions += [new_head_position]
                self.game.board.apples.remove(apple)
                self.game.board.spawn_apple()
                return
        self.positions = self.positions[1:] + [new_head_position]

    def render(self, display: Surface) -> None:
        for k, pos in enumerate(self.positions[:-1]):
            rect = get_cell_rect(pos[0], pos[1])
            color = (lerp(20, 100, 10 / (len(self.positions) - k - 1)),
                     lerp(30, 180, 10 / (len(self.positions) - k - 1)),
                     lerp(20, 100, 10 / (len(self.positions) - k - 1)))
            pygame.draw.rect(display, color, rect, 0)

        head_rect = get_cell_rect(self.positions[-1][0], self.positions[-1][1])
        pygame.draw.rect(display, (0, 255, 0), head_rect, 0)


class Apple:
    def __init__(self, x, y):
        self.pos = (x, y)

    def check_eat(self, snake_pos: tuple[int, int]) -> bool:
        return snake_pos == self.pos

    def render(self, display: Surface) -> None:
        rect = get_cell_rect(self.pos[0], self.pos[1])
        pygame.draw.rect(display, (175, 60, 60), rect, 0)
