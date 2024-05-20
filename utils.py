from random import randint

from settings import BOARD_OFFSET, CELL_SIZE, SNAKE_OFFSET, BOARD_SIZE


def get_cell_rect(x: int, y: int) -> tuple[int, int, int, int]:
    return (BOARD_OFFSET + CELL_SIZE * x + SNAKE_OFFSET, BOARD_OFFSET + CELL_SIZE * y + SNAKE_OFFSET,
            CELL_SIZE - SNAKE_OFFSET * 2, CELL_SIZE - SNAKE_OFFSET * 2)


def lerp(a: int, b: int, step: float) -> int:
    return round(a + (abs(step) / 10) * (b - a))


def random_coordinates() -> tuple[int, int]:
    return randint(0, BOARD_SIZE[0] - 1), randint(0, BOARD_SIZE[1] - 1)
