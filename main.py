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
            (' ' + text_index if len(text_index) == 1 else text_index) + '   ' +
            '  '.join([str(point) for point in line])
        )
    print('')


def fill_board_random(board):
    ship_to_place = 1
    while ship_to_place < 6:
        if place_ship(board, randint(0, 9), randint(0, 9), 'v' if randint(0, 1) == 1 else 'h', ship_to_place):
            ship_to_place += 1


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
            if board_line > (line - 1) and board_line < line + ship_size:
                board[board_line][col] = ship_id
    
    return True


# ---------- USER INPUT HELPERS ----------


def user_add_ship(board, ship_id):
    ship_size = get_ship_data(ship_id)[2]

    print(f'\n\nPositionning your ship of length {ship_size}\n')

    placed = False

    while not placed:
        display_board(board)
        line, col, direction = 0, 0, 0
        
        # Column
        while col not in axis_indices['x']:
            col = input('Column (between A and J) : ').upper()
            if col not in axis_indices['x']:
                print(f'Invalid column "{col}"')
        col = axis_indices['x'].index(col)

        # Line
        while not (line >= 1 and line <= 10):
            line = int(input('Line (between 1 and 10) : '))
            if line < 1 or line > 10:
                print(f'Invalid line "{line}"')
        line -= 1

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
    display_board(board1)
    user_add_all_ships(board1)
    display_board(board1)
