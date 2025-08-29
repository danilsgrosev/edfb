BOARD_SIZE = 1280
CORNER_SIZE = 128
SIDE_CELL_WIDTH = 96
SIDE_CELL_HEIGHT = 128

def generate_board_cells():
    coords = []

    # Нижняя сторона (0–10): справа налево
    for i in range(10):
        x = BOARD_SIZE - CORNER_SIZE - SIDE_CELL_WIDTH * i
        y = BOARD_SIZE - CORNER_SIZE
        coords.append((x, y))

    # Левая сторона (11–20): снизу вверх
    for i in range(1, 10):
        x = 0
        y = BOARD_SIZE - CORNER_SIZE - SIDE_CELL_HEIGHT * i
        coords.append((x, y))
    coords.append((0, 0))  # Free Parking

    # Верхняя сторона (21–30): слева направо
    for i in range(1, 10):
        x = CORNER_SIZE + SIDE_CELL_WIDTH * (i - 1)
        y = 0
        coords.append((x, y))
    coords.append((BOARD_SIZE - CORNER_SIZE, 0))  # Go To Jail

    # Правая сторона (31–39): сверху вниз
    for i in range(1, 10):
        x = BOARD_SIZE - CORNER_SIZE
        y = CORNER_SIZE + SIDE_CELL_HEIGHT * (i - 1)
        coords.append((x, y))

    board_cells = []
    for i, (x, y) in enumerate(coords):
        board_cells.append({
            "id": i,
            "x": x,
            "y": y,
            "width": CORNER_SIZE if i % 10 == 0 else SIDE_CELL_WIDTH,
            "height": CORNER_SIZE if i % 10 == 0 else SIDE_CELL_HEIGHT
        })

    return board_cells
