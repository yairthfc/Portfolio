#################################################################
# FILE : puzzle_solver.py
# WRITER : yair mahfud , yairthfc ,207807082
# EXERCISE : intro2cs ex8 2022-2023
# DESCRIPTION: a program of a game called black and white puzzle solver using backtracking
# STUDENTS I DISCUSSED THE EXERCISE WITH: no one
# WEB PAGES I USED:
# NOTES: 
#################################################################
from typing import List, Tuple, Set, Optional


# We define the types of a partial picture and a constraint (for type checking).
Picture = List[List[int]]
Constraint = Tuple[int, int, int]
BLACK = 0
WHITE = 1
UNKNOWN = -1


def max_seen_cells(picture: Picture, row: int, col: int) -> int:
    """takes a picture and index and check the number of max seen cells from it"""
    counter = 0
    if picture[row][col] == BLACK:
        return 0
    else:
        counter += 1
    for back in range(1, col + 1):
        if picture[row][col - back] != BLACK:
            counter += 1
        else :
            break
    for forward in range(1, len(picture[0]) - col):
        if picture[row][col + forward] != BLACK:
            counter += 1
        else :
            break
    for up in range(1, row + 1):
        if picture[row - up][col] != BLACK:
            counter += 1
        else :
            break
    for down in range(1, len(picture) - row):
        if picture[row + down][col] != BLACK:
            counter += 1
        else :
            break
    return counter



def min_seen_cells(picture: Picture, row: int, col: int) -> int:
    """takes a picture and index and returns the minimum of seen cells from it"""
    counter = 0
    if picture[row][col] == BLACK or picture[row][col] == UNKNOWN:
        return 0
    else:
        counter += 1
    for back in range(1, col + 1):
        if picture[row][col - back] != BLACK and picture[row][col - back] != UNKNOWN:
            counter += 1
        else :
            break
    for forward in range(1, len(picture[0]) - col):
        if picture[row][col + forward] != BLACK and picture[row][col + forward] != UNKNOWN:
            counter += 1
        else :
            break
    for up in range(1, row + 1):
        if picture[row - up][col] != BLACK and picture[row - up][col] != UNKNOWN:
            counter += 1
        else :
            break
    for down in range(1, len(picture) - row):
        if picture[row + down][col] != BLACK and picture[row + down][col] != UNKNOWN:
            counter += 1
        else :
            break
    return counter


def check_constraints(picture: Picture, constraints_set: Set[Constraint]) -> int:
    """checks if the constraints given are in line with the picture given and returns a number according to it"""
    counter = 0
    for value in constraints_set:
        row, column, seen = value
        if seen < min_seen_cells(picture, row, column) or seen > max_seen_cells(picture, row, column):
            return 0
        elif seen == min_seen_cells(picture, row, column) and seen == max_seen_cells(picture, row, column):
            counter += 1
    if counter == len(constraints_set):
        return 1
    else:
        return 2

def create_board(n: int, m: int) -> Picture:
    """creates a board with n rows and n colums filled with UNKNOWN in each index"""
    board = []
    for x in range(n):
        list1 = []
        for y in range(m):
            list1.append(UNKNOWN)
        board.append(list1)
    return board

def solve_puzzle(constraints_set: Set[Constraint], n: int, m: int) -> Optional[Picture]:
    """gets a constraints set and row and columns number and calls functions that creates the board and
    helps solve the puzzle and returns the solved puzzle"""
    board = create_board(n, m)
    solution = helper_solve_puzzle(constraints_set, board,0)
    return solution

def helper_solve_puzzle(constraints_set: set[Constraint], board: Picture,ind: int) -> Optional[Picture]:
    """gets a constraintes set and a board fillled with UNKNOWN and changes the value for each index,
    to black or white and if it works continues to the next index, else it chnanges again the value
    or goes back to change the value of the previous until it gets the solved board"""
    if check_constraints(board, constraints_set) == 0:
        return 
    if ind == len(board) * len(board[0]):
        return board
    row, col = ind // len(board[0]), ind % len(board[0])
    for x in [BLACK,WHITE]:
        board[row][col] = x
        if check_constraints(board, constraints_set) == 1 or check_constraints(board, constraints_set) == 2:
            solution = helper_solve_puzzle(constraints_set, board,ind +1)
            if solution != None:
                return solution
    board[row][col] = UNKNOWN

def how_many_solutions(constraints_set: Set[Constraint], n: int, m: int) -> int:
    """gets a constraints set and row and columns number and calls functions that creates the board and
    helps get the number of solutions possible"""
    board = create_board(n, m)
    solution = helper_many_sol(constraints_set, board,0)
    return solution

def helper_many_sol(constraints_set: Set[Constraint], board: Picture,ind: int) -> int:
    """gets a constraintes set and a board fillled with UNKNOWN and changes the value for each index,
    to black or white and if it works continues to the next index, else it chnanges again the value
    or goes back to change the value of the previous until it gets to the end of the board and adds to the counter.
    at the end the counter is returned with the number of solutions"""
    if check_constraints(board, constraints_set) == 0:
        return 
    if ind == len(board) * len(board[0]):
        return 1
    counter = 0
    row, col = ind // len(board[0]), ind % len(board[0])
    for x in [BLACK,WHITE]:
        board[row][col] = x
        if check_constraints(board, constraints_set) == 1 or check_constraints(board, constraints_set) == 2:
            solution = helper_many_sol(constraints_set, board,ind +1)
            if solution != None:
                counter += solution
    board[row][col] = UNKNOWN
    return counter

def generate_puzzle(picture: Picture) -> Set[Constraint]:
    """gets a puzzle and gets all the constraints from it and then calls the filterer to get the minimum
    needed constraints"""
    cons_set = set()
    helper_gen_puz(picture,cons_set, 0)
    outcome = filterer(picture, cons_set)
    return outcome

def filterer(picture: Picture, cons_set: Set[Constraint]) -> Set[Constraint]:
    """filters all the constraints given according to the comparence of the original solved puzzle
    and number of solutions against the current without a certain constraint and decides to keep it
    if its needed"""
    solved = solve_puzzle(cons_set, len(picture), len(picture[0]))
    num_sol = how_many_solutions(cons_set, len(picture), len(picture[0]))
    constantin = set()
    for i in cons_set:
        constantin.add(i)
    for x in cons_set:
        constantin.remove(x)
        cur_solved = solve_puzzle(constantin, len(picture), len(picture[0]))
        cur_num_sol = how_many_solutions(constantin, len(picture), len(picture[0]))
        if solved != cur_solved or num_sol != cur_num_sol:
            constantin.add(x)
        else:
            pass
    return constantin

def helper_gen_puz(picture: Picture, cons_set: Set[Constraint], ind: int) -> int:
    """gets a picture and an empty cons set and goes through every index to determine its needed 
    constraint to comply with the max seen cells and check constraints and returns the full cons set"""
    if check_constraints(picture, cons_set) == 0:
        return
    if ind == len(picture) * len(picture[0]):
        return 1
    row, col = ind // len(picture[0]), ind % len(picture[0])
    if picture[row][col] == 1:
        numbit = max_seen_cells(picture, row, col)
        for x in range(1,numbit + 1):
            cons = (row,col,x)
            cons_set.add(cons)
            if check_constraints(picture, cons_set) == 1 or check_constraints(picture, cons_set) == 2:
                solution = helper_gen_puz(picture, cons_set, ind + 1) 
                if solution != None:
                    return solution
            else:
                cons_set.remove(cons)
    else:
        cons = (row, col, 0)
        cons_set.add(cons)
        return helper_gen_puz(picture,cons_set, ind + 1)