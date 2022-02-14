from random import randint


# ---------- BOARD HELPERS ----------

def generate_board():
    return [[0] * 10 for i in range(10)]


axis_indices = {
    'x': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
    'y': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
}


def display_board(board):
    print(' ' * 5 + '  '.join(axis_indices['x']))
    for index, line in enumerate(board):
        text_index = axis_indices['y'][index]
        print(
            (' ' + text_index if len(text_index) == 1 else text_index)
            + '   '
            + '  '.join([str(point) for point in line])
        )
    print('')


def fill_board_random(board):
    ship_to_place = 1
    while ship_to_place < 6:
        if place_ship(board, randint(0, 9), randint(0, 9), 'v' if randint(0, 1) == 1 else 'h', ship_to_place):
            ship_to_place += 1


def attack(board, line, col):
    point = board[line][col]

    if point == 0:
        print('Miss!')
        return
    elif point == 6:
        print('Already touched!')
        return

    board[line][col] = 6

    if is_ship_sunk(board, point):
        print('Sunk!')
    else:
        print('Hit!')


def is_lost(board):
    return not any([any([col != 0 and col != 6 for col in line]) for line in board])


# ---------- SHIPS HELPERS ----------

ships = [
    ['porte-avion', 1, 5],
    ['croiseur', 2, 4],
    ['contre-torpilleurs', 3, 3],
    ['sous-marin', 4, 3],
    ['torpilleu', 5, 2],
]


def get_ship_data(ship_id):
    for ship in ships:
        if ship[1] == ship_id:
            return ship


def place_ship(board, line, col, direction, ship_id):
    ship_size = get_ship_data(ship_id)[2]

    # Getting the points where the ship should be placed
    if direction == 'h':
        board_region = board[line][col:(col + ship_size)]
    else:
        board_region = [board_line[col] for board_line in board][line:(line + ship_size)]

    # If the result region is smaller than the ship size,
    # it means that the end of the ship is out of bounds
    if len(board_region) != ship_size:
        return False

    # Tests if all points are empty
    if not all(point == 0 for point in board_region):
        return False

    # Place the ship
    if direction == 'h':
        board[line][col:(col + ship_size)] = [ship_id] * ship_size
    else:
        for board_line in range(10):
            if (line - 1) < board_line < line + ship_size:
                board[board_line][col] = ship_id

    return True


def is_ship_sunk(board, ship_id):
    return not any([ship_id in line for line in board])


def ai_play_dumb(board):
    line, col = None, None
    # Prevents selecting already touched places
    while line is None or col is None or board[line][col] == 6:
        line, col = randint(0, 9), randint(0, 9)
    return line, col


# ---------- USER INPUT HELPERS ----------


def ask_coordinate():
    col, line = 0, 0

    # Column
    while col not in axis_indices['x']:
        col = input('Column (between A and J) : ').upper()
        if col not in axis_indices['x']:
            print(f'Invalid column "{col}"')
    col = axis_indices['x'].index(col)

    # Line
    while not (1 <= line <= 10):
        line = int(input('Line (between 1 and 10) : '))
        if line < 1 or line > 10:
            print(f'Invalid line "{line}"')
    line -= 1

    return line, col


def user_add_ship(board, ship_id):
    ship_size = get_ship_data(ship_id)[2]

    print(f'\n\nPositionning your ship of length {ship_size}\n')

    placed = False

    while not placed:
        display_board(board)

        direction = 0
        col, line = ask_coordinate()

        # Direction
        while direction != 'v' and direction != 'h':
            direction = input('Direction (v for vertical or h for horizontal) : ').lower()
            if direction != 'v' and direction != 'h':
                print(f'Invalid direction "{direction}"')

        placed = place_ship(board, line, col, direction, ship_id)

        if not placed:
            print('\n\nCan\'t place ship here, please retry\n')


def user_add_all_ships(board):
    ship_id = 1
    while ship_id <= 5:
        user_add_ship(board, ship_id)
        ship_id += 1



# ---------- GAME LOOP ----------

board1 = generate_board()
board2 = generate_board()


if __name__ == '__main__':
    fill_board_random(board1)
    display_board(board1)

    while not is_lost(board1):
        line, col = ai_play_dumb(board1)
        attack(board1, line, col)
    display_board(board1)
