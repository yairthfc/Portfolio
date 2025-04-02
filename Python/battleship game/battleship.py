#############################################################
# FILE : battleship.py
# WRITER : Yair Mahfud , yairthfc , 207807082
# EXERCISE : intro2cs1 ex4 2023
# PEOPLE I DISCUSSED WITH : no one
#############################################################
import helper
from copy import deepcopy

def init_board(rows, columns):
    """creates a simple board filled with 'water' """
    board = []
    for x in range(rows):
        list1 = []
        for y in range(columns):
            list1.append(helper.WATER)
        board.append(list1)
    return board

def is_number(string):
    """verifys if a string is a number between 1 and 99"""
    list_of_nums = []
    for x in range(1,100):
        x = str(x)
        list_of_nums.append(x)
    if string in list_of_nums :
        return True
    else :
        return False

def cell_loc(loc):
    """takes a string, and returns a tuple with the matching cordinates"""
    if (1 < len(loc) < 4):
        letter = loc[:1]
        str_number = loc[1:]
        position = ord(letter)
        if is_number(str_number) and letter.isalpha() and (64 < position < 91) :
            number = int(str_number)
            index = (number - 1),(position - 65)
            if (0 < number <= 99):
                return index
            else:
                return None
        else:
            return None

def valid_ship(board, size, loc):
    """validates if a ship fits the board and if the location is avilable"""
    if (loc[0] + size <= len(board)) and (loc[1] < len(board[0])):
        for index in range(0, size):
            if board[loc[0]+index][loc[1]] != helper.WATER :
                return False
            else:
                continue
        return True
    return False

def create_player_board(rows, columns, ship_sizes):
    """creates the board of the user with the correct inputs given by him and returns the full board"""
    final_board = init_board(rows,columns)
    for ship_len in ship_sizes:
        val_ship_loc = 1
        if ship_len > rows:
            continue
        while val_ship_loc == 1 :
            helper.print_board(final_board)
            ship_loc = helper.get_input("enter your ship cordinates: ")
            user_cord = cell_loc(ship_loc)
            if user_cord == None:
                print("please enter ship in valid location.")
            else :
                if valid_ship(final_board,ship_len,user_cord):
                    for n in range(ship_len):
                        final_board[user_cord[0]+n][user_cord[1]] = helper.SHIP
                        val_ship_loc = 0
                else:
                    print("please enter ship in valid location.")
    return final_board

def fire_torpedo(board,loc):
    """a function that shoots a torpedo to an index ,changes the index value and returns the correct board"""
    board = board
    if loc[0] <= len(board) and loc[1] <= len(board[0]) :
        if board[loc[0]][loc[1]] == helper.WATER:
            board[loc[0]][loc[1]] = helper.HIT_WATER
        elif board[loc[0]][loc[1]] == helper.SHIP:
            board[loc[0]][loc[1]] = helper.HIT_SHIP
    else:
        pass
    return board

def create_comp_board(board):
    """creates the computer board while make sures that its in a avilable index"""
    ship_sizes = helper.SHIP_SIZES 
    board = board 
    for z in ship_sizes:
        pos_loc = set()
        for x in range((helper.NUM_ROWS) - z + 1):
            for y in range((helper.NUM_COLUMNS)):
                validator = 0
                for i in range(z):
                    if board[x+i][y] == helper.WATER:
                        validator += 1
                        continue
                if validator == z:
                    pos_loc.add((x, y))
        if z <= len(board):
            chosen_loc = helper.choose_ship_location(board, z, pos_loc)
            for n in range(z):
                board[chosen_loc[0]+n][chosen_loc[1]] = helper.SHIP
    return board

def hidden_board(board):
    """takes a full board and creates and returns a different, hidden board to it showing only water"""
    board_rep = deepcopy(board)
    for row in range(helper.NUM_ROWS):
        for column in range(helper.NUM_COLUMNS):
            if board[row][column] == helper.SHIP:
                board_rep[row][column] = helper.WATER
    return board_rep

def are_ships_destroyed(board):
    """checks if all ships on the board are destroyed and returns a boolean value"""
    for row in range(helper.NUM_ROWS):
        for column in range(helper.NUM_COLUMNS):
            if board[row][column] == helper.SHIP:
                return False
            else:
                continue
    return True

def insert_valid_torpedo(board):
    """gets an input fron the user of a torpedo index, validates that its compatible and returns
    the index of the user input"""
    counter = 1
    while counter == 1:
        user_input = helper.get_input("insert torpedo target: ")
        letter = user_input[:1]
        str_number = user_input[1:]
        if 1 < len(user_input) < 4 and is_number(str_number) and letter.isalpha():
            letter = letter.upper()
            if (ord(letter) - 65) <= helper.NUM_COLUMNS and int(str_number) <= helper.NUM_ROWS:
                number = int(str_number)
                cordinates = number -1, (ord(letter) - 65)
                if board[cordinates[0]][cordinates[1]] != helper.HIT_SHIP and board[cordinates[0]][cordinates[1]] != helper.HIT_WATER:
                    counter = 2
                    return cordinates
                else:
                    print("please insert valid target")
            else:
                print("please insert valid target")
        else:
            print("please insert valid target")

def comp_possible_torpedo(board):
    """gets a board and calculates the possible locations to shoot a torpedo for the computer"""
    pos_loc = set()
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] != helper.HIT_SHIP and board[x][y] != helper.HIT_WATER:
                position = x,y
                pos_loc.add(position)
    return pos_loc

def player_turn(comp_board):
    """playes the player turn and changes the computer board acoording to the torpedo hit"""
    user_fire = insert_valid_torpedo(comp_board)
    if comp_board[user_fire[0]][user_fire[1]] == helper.WATER:
        comp_board[user_fire[0]][user_fire[1]] = helper.HIT_WATER
    elif comp_board[user_fire[0]][user_fire[1]] == helper.SHIP:
        comp_board[user_fire[0]][user_fire[1]] = helper.HIT_SHIP

def comp_turn(user_board):
    """playes the computer turn and changes the player board according to the torpedo hit"""
    comp_fire = helper.choose_torpedo_target(hidden_board(user_board),comp_possible_torpedo(hidden_board(user_board)))
    if user_board[comp_fire[0]][comp_fire[1]] == helper.WATER:
        user_board[comp_fire[0]][comp_fire[1]] = helper.HIT_WATER
    elif user_board[comp_fire[0]][comp_fire[1]] == helper.SHIP:
        user_board[comp_fire[0]][comp_fire[1]] = helper.HIT_SHIP

def main():
    """a function that runs the course of the game.prints the board,play the turns,detrmins the winner
    and after the game finishes asks the player if he wants to play another game"""
    restart_val = "Y"
    while restart_val == "Y":
        user_board = create_player_board(helper.NUM_ROWS, helper.NUM_COLUMNS, helper.SHIP_SIZES)
        comp_board = create_comp_board(init_board(helper.NUM_ROWS, helper.NUM_COLUMNS))
        helper.print_board(user_board,hidden_board(comp_board))
        pos_winner = 1
        while True:
            player_turn(comp_board)
            if are_ships_destroyed(comp_board):
                pos_winner = 1
            comp_turn(user_board)
            if are_ships_destroyed(user_board):
                pos_winner = 2
            if are_ships_destroyed(comp_board) and are_ships_destroyed(user_board):
                pos_winner = 3
            if are_ships_destroyed(user_board) or are_ships_destroyed(comp_board):
                break
            helper.print_board(user_board,hidden_board(comp_board))
        helper.print_board(user_board,comp_board)
        if pos_winner == 1:
            print("user has won the game!")
        elif pos_winner == 2:
            print("computer has won the game!")
        ask_question = "no"
        while ask_question == "no":
            restart = helper.get_input("do you want to play again?")
            if restart in ("Y","N"):
                restart_val = restart
                ask_question = "yes"
            else:
                print("please enter valid syntex")


if __name__=="__main__":
    main()