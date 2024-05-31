from random import randint

import settings


def get_cell_rect(x: int, y: int) -> tuple[int, int, int, int]:
    board_offset = settings.BOARD_OFFSET
    snake_offset = settings.SNAKE_OFFSET
    cell_size = settings.CELL_SIZE
    return (board_offset + cell_size * x + snake_offset, board_offset + cell_size * y + snake_offset,
            cell_size - snake_offset * 2, cell_size - snake_offset * 2)


def lerp(a: int, b: int, step: float) -> int:
    return round(a + abs(step) * (b - a))


def random_coordinates() -> tuple[int, int]:
    width, height = settings.BOARD_SIZE
    return randint(0, width - 1), randint(0, height - 1)


def random_available_cell(board) -> tuple[int, int]:
    while not board.can_win():
        pos = random_coordinates()
        if pos in board.snake.positions or \
                pos in map(lambda x: x.pos, board.walls) or \
                pos in map(lambda x: x.pos, board.apples):
            continue
        return pos
