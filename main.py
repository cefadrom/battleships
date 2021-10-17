# ---------- BOARD HELPERS ----------

def generate_board():
    return [[0] * 10] * 10


axis_indices = {
    'x': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
    'y': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
}

def display_board(board):
    print(' ' * 5 + '  '.join(axis_indices['x']))
    for index, line in enumerate(board):
        text_index = axis_indices['y'][index]
        print(
            (' ' + text_index if len(text_index) == 1 else text_index) + '   ' +
            '  '.join([str(point) for point in line])
        )
    print('')


# ---------- GAME LOOP ----------

board1 = generate_board()
board2 = generate_board()


if __name__ == '__main__':
    display_board(board1)
