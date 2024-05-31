import pygame
from pygame import Surface

import settings
from utils import get_cell_rect, lerp, random_coordinates, random_available_cell


class Board:
    """
    Класс, отвечающий за игровое поле.
    """
    def __init__(self, game):
        self.game = game

        self.snake = Snake(game)
        self.apples: list[Apple] = []
        self.walls: list[Wall] = []

    def reset(self):
        """
        Сброс игрового поля.
        :return: Ничего
        """
        self.snake.reset()
        self.snake.positions.append((2, 2))

        self.walls.clear()
        self.spawn_walls()

        self.apples.clear()
        for i in range(settings.APPLE_AMOUNT):
            self.spawn_apple()

    def spawn_apple(self):
        """
        Создать яблоко на поле.
        :return: Ничего
        """
        if self.can_win():
            return
        pos = random_available_cell(self)
        apple = Apple(*pos)
        self.apples.append(apple)

    def spawn_walls(self):
        """
        Создать стены на поле.
        :return: Ничего
        """
        wall_amount = settings.WALL_AMOUNT
        for i in range(wall_amount):
            pos = random_available_cell(self)
            wall = Wall(*pos)
            self.walls.append(wall)

    def update(self) -> None:
        """
        Обновление игрового поля.
        :return: Ничего
        """
        self.snake.move()
        self.check_win()

    def can_win(self) -> None:
        """
        Проверка на победу в игре.
        :return: Победил ты или нет.
        """
        width, height = settings.BOARD_SIZE
        wall_amount = settings.WALL_AMOUNT
        return len(self.snake.positions) == (width * height) - wall_amount

    def check_win(self) -> None:
        """
        Проверка на победу в игре.
        :return: Ничего
        """
        if self.can_win():
            self.game.win()

    @staticmethod
    def render(display) -> None:
        """
        Отрисовка игрового поля.
        :param display: :class:`Surface` на котором нужно отрисовать поле.
        :return: Ничего
        """
        display.fill((0, 0, 0))
        width, height = settings.BOARD_SIZE
        offset = settings.BOARD_OFFSET
        cell_size = settings.CELL_SIZE
        for x in range(width + 1):
            pygame.draw.line(display, (255, 255, 255),
                             (offset + x * cell_size, offset),
                             (offset + x * cell_size, offset + height * cell_size))
        for y in range(height + 1):
            pygame.draw.line(display, (255, 255, 255),
                             (offset, offset + y * cell_size),
                             (offset + width * cell_size, offset + y * cell_size))


class Snake:
    """
    Класс, отвечающий за отрисовку змеи и её передвижение.
    """
    def __init__(self, game):
        self.game = game

        self.last_direction = None
        self.direction = (0, 0)
        self.positions = []

    def reset(self) -> None:
        """
        Сброс всех переменных.
        :return: Ничего
        """
        self.last_direction = None
        self.direction = (0, 0)
        self.positions = []

    def set_direction(self, direction: tuple[int, int]) -> None:
        """
        Изменение направления движения змеи.
        :param direction: Вектор направления
        :return: Ничего
        """
        x, y = direction
        if self.last_direction is not None and sum(self.last_direction) != 0:
            if self.last_direction[0] == x * -1 or self.last_direction[1] == y * -1:
                return
        self.direction = (x, y)

    def move(self) -> None:
        """
        Передвижение змеи.
        :return: Ничего
        """
        if self.direction == (0, 0):
            return

        width, height = settings.BOARD_SIZE
        new_head_position = self.positions[-1][0] + self.direction[0], self.positions[-1][1] + self.direction[1]
        # Столкновение с рамками, или собой.
        if (new_head_position[0] < 0 or new_head_position[0] >= width) or \
                (new_head_position[1] < 0 or new_head_position[1] >= height) or \
                new_head_position in self.positions[1:]:
            self.game.lose()
            return
        # Столкновение со стенами.
        for wall in self.game.board.walls:
            if wall.check_collision(new_head_position):
                self.game.lose()
                return
        # Взаимодействие с яблоками.
        for apple in self.game.board.apples:
            if apple.check_collision(new_head_position):
                self.positions += [new_head_position]
                self.game.board.apples.remove(apple)
                self.game.board.spawn_apple()
                return
        self.positions = self.positions[1:] + [new_head_position]
        self.last_direction = self.direction

    def render(self, display: Surface) -> None:
        """
        Отрисовка змеи.
        :param display: :class:`Surface` на котором нужно отрисовать змею.
        :return: Ничего
        """
        for k, pos in enumerate(self.positions[:-1]):
            rect = get_cell_rect(pos[0], pos[1])

            mu = 1 / abs(len(self.positions) - k - 1)
            color = (lerp(40, 130, mu),
                     lerp(60, 180, mu),
                     lerp(40, 130, mu))

            pygame.draw.rect(display, color, rect, 0)

        head_rect = get_cell_rect(self.positions[-1][0], self.positions[-1][1])
        pygame.draw.rect(display, (0, 255, 0), head_rect, 0)


class InteractableObject:
    def __init__(self, x, y):
        self.pos = (x, y)

    def check_collision(self, pos):
        return self.pos == pos

    def get_pos(self):
        return self.pos


class Apple(InteractableObject):
    """
    Класс, отвечающий за отрисовку и поедание яблок.
    """
    def __init__(self, x, y):
        super().__init__(x, y)

    def render(self, display: Surface) -> None:
        """
        Отрисовка яблока.
        :param display: :class:`Surface` на котором нужно отрисовать яблоко.
        :return: Ничего
        """
        rect = get_cell_rect(self.pos[0], self.pos[1])
        pygame.draw.rect(display, (175, 60, 60), rect, 0)


class Wall(InteractableObject):
    """
    Класс, отвечающий за отрисовку стен и столкновением с ними.
    """
    def __init__(self, x, y):
        super().__init__(x, y)

    def render(self, display):
        """
        Отрисовка стены.
        :param display: :class:`Surface` на котором нужно отрисовать яблоко.
        :return: Ничего
        """
        rect = get_cell_rect(self.pos[0], self.pos[1])
        pygame.draw.rect(display, (70, 70, 70), rect, 0)
