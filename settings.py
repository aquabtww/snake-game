# Настройки игрового поля
BOARD_OFFSET = 75

BOARD_SIZE = [6, 6]
CELL_SIZE = 50

WALL_AMOUNT = 2
APPLE_AMOUNT = 1

UPDATE_SPEED = 300

# Константы
SNAKE_OFFSET = CELL_SIZE // 8
FPS = 120


def add_speed():
    global UPDATE_SPEED
    UPDATE_SPEED = max(10, UPDATE_SPEED + 10)


def take_speed():
    global UPDATE_SPEED
    UPDATE_SPEED = max(10, UPDATE_SPEED - 10)


def add_width():
    global BOARD_SIZE
    BOARD_SIZE[0] = max(3, BOARD_SIZE[0] + 1)


def take_width():
    global BOARD_SIZE
    BOARD_SIZE[0] = max(3, BOARD_SIZE[0] - 1)


def add_height():
    global BOARD_SIZE
    BOARD_SIZE[1] = max(3, BOARD_SIZE[1] + 1)


def take_height():
    global BOARD_SIZE
    BOARD_SIZE[1] = max(3, BOARD_SIZE[1] - 1)


def add_wall():
    global WALL_AMOUNT
    WALL_AMOUNT = min(WALL_AMOUNT + 1, 5)


def take_wall():
    global WALL_AMOUNT
    WALL_AMOUNT = max(0, WALL_AMOUNT - 1)


def add_apple():
    global APPLE_AMOUNT
    APPLE_AMOUNT = min(APPLE_AMOUNT + 1, 5)


def take_apple():
    global APPLE_AMOUNT
    APPLE_AMOUNT = max(1, APPLE_AMOUNT - 1)
