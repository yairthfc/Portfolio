#!/usr/bin/env python3

# import sys
import random
import time
import battleship

start_time = time.time()

NUM_ROWS = 2
NUM_COLUMNS = 3
SHIP_SIZES = (2, 2)

WATER = 5
SHIP = 6
HIT_WATER = 7
HIT_SHIP = 8

RED = "\033[7;31m"
BLUE = "\033[7;34m"
CYAN = "\033[7;36m"
BROWN = "\033[7;33m"
MAGENTA = "\033[7;35m"
RESET = "\033[0m"

# if sys.stdout.isatty():
print_mapping = {WATER: f'{BLUE}. {RESET}',
                 SHIP: f'{BROWN}x {RESET}',
                 HIT_WATER: f'{CYAN}o {RESET}',
                 HIT_SHIP: f'{RED}* {RESET}',
                 }
err_str = f'{MAGENTA}? {RESET}'
"""else:
    print_mapping = {WATER: '. ',
                     SHIP: 'x ',
                     HIT_WATER: 'o ',
                     HIT_SHIP: '* ',
                     }
    err_str = '? '"""


def str_row(board, i):
    if i < len(board):
        return (str(i + 1).rjust(2) + ' ' +
                ''.join(print_mapping.get(board[i][j], err_str) for j in
                        range(len(board[i]))))
    else:
        return ''


def print_board(board1, board2=None):
    '''Prints a clear board and a hidden board side by side.
    If board2 is None, prints only a clear board.
    Assumes the boards are valid.
    Will work for boards with at most 99 rows and 26 columns'''
    boards = [board1] if board2 is None else [board1, board2]
    header = "   " + ''.join(
        [chr(j + ord('A')) + ' ' for j in range(len(board1[0]))])
    sep = 10 * ' '
    print(*(header for board in boards), sep=sep)
    for i in range(max(len(board) for board in boards)):
        print(*(str_row(board, i) for board in boards), sep=sep)


inputs = ["N", "B2", "A2", "C1", "B1", "A1", "B1", "A1"]


def get_input(msg):
    print(msg)
    i=inputs.pop()
    print(i)
    return i


def is_int(s):
    '''Checks if a string can be casted to an integer'''
    try:
        int(s)
        return True
    except ValueError:
        return False


def random_cell(cells):
    return random.choice(sorted(cells))


def choose_ship_location(board, size, locations):
    print("...")
    '''Choose a location for a ship.
    locations is the set of valid placements.
    (locations are indexes (e.g., (0,1)) and not names (e.g., 'A2').)
    board and size are provided for alternate non random computer players.
    '''
    print(sorted(locations))
    return sorted(locations)[0]


def choose_torpedo_target(board, locations):
    print(".......")
    '''Choose a target for firing a torpedo.
    locations is the set of valid targets.
    board is provided for alternate non random computer players and should not show hidden ships.
    '''
    print(sorted(locations))
    return sorted(locations)[0]


def seed(a):
    '''Set seed for reproducible games'''
    random.seed(a)


if __name__ == "__main__":
    battleship.main()
    print(time.time() - start_time)
