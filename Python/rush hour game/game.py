#################################################################
# FILE : game.py
# WRITER : yair mahfud , yairthfc ,207807082
# EXERCISE : intro2cs ex9 2022-2023
# DESCRIPTION: A game called rush hour using classes
# STUDENTS I DISCUSSED THE EXERCISE WITH: no one
# WEB PAGES I USED:
# NOTES: 
#################################################################
import helper
from board import Board
import car
import sys
import json

class Game:
    """
    Add class description here
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        # You may assume board follows the API
        # implement your code and erase the "pass"
        self.__board = board
        


    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        # implement your code and erase the "pass"


    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        # implement your code and erase the "pass"
        while True:
            print(self.__board)
            target = self.__board.target_location()
            if self.__board.cell_content(target) != None:
                break
            user_input = input("please enter car name and direction: ")
            if user_input == "!":
                break
            legal_names = "YBOGWR"
            legal_moves = "udlr"
            if len(user_input) == 3 and user_input[0] in legal_names and user_input[2] in legal_moves and user_input[1] == ",":
                name, direct = user_input.split(",")
                if name in self.__board.get_car_dict():
                    self.__board.move_car(name,direct)


if __name__== "__main__":
    # Your code here
    # All access to files, non API constructors, and such must be in this
    # section, or in functions called from this section.
    # implement your code and erase the "pass"
    args = sys.argv
    car_conf = helper.load_json(args[1])
    board = Board()
    possible_names = ('Y','B','O','W','G','R')
    for carr in car_conf:
        car_val = car_conf[carr]
        length = car_val[0]
        st_loc = car_val[1]
        orientation = car_val[2]
        if (1 < length < 5) and (-1 < orientation < 2) and carr in possible_names:
            car_name = car.Car(carr, length, st_loc, orientation)
            board.add_car(car_name)
    game = Game(board)
    game.play()