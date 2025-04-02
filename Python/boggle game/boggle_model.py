from boggle_board_randomizer import randomize_board
from ex11_utils import *
import tkinter as tki
from typing import Dict, List, Set, Iterable, Tuple
from pprint import pprint


class BoggleModel:
    """The model for the Boggle game."""

    def __init__(self, words: Iterable[str]) -> None:
        self.__board: Board = randomize_board()
        self.__current_word: str = ""
        self.__score: int = 0
        self.__words: List[str] = []
        self.__valid_words: Iterable[str] = words
        self.__path: Path = []
        self.__start_time: int = 180_000

    def add_letter(self, button_loc: Location) -> None:
        """Adds the letter at the given button location to the current word if
           it's valid, and resets the word and path to be empty otherwise."""
        if (self.__path == [] or valid_move(self.__path[-1], button_loc)) and \
                button_loc not in self.__path:
            self.__current_word += self.__board[button_loc[0]][button_loc[1]]
            self.__path.append(button_loc)

    def add_word(self) -> None:
        """Adds the word to the word set if it's a valid word, and adds to the
           score accordingly."""
        if self.__current_word in list(self.__valid_words) and \
                self.__current_word not in self.__words:
            self.__score += len(self.__current_word)**2
            self.__words.append(self.__current_word)
        self.__current_word = ""
        self.__path = []

    def get_score(self) -> int:
        """Returns the current score."""
        return self.__score

    def get_max_score(self) -> int:
        """Returns the highest possible score to get from the board."""
        paths = max_score_paths(self.__board, self.__valid_words)
        max_score = 0
        for path in paths:
            max_score += len(path)**2
        return max_score

    def get_board(self) -> Board:
        return self.__board

    def get_words(self) -> List[str]:
        """Returns the set of all valid words that were found."""
        return self.__words

    def all_valid_words(self) -> List[str]:
        """Returns a list of words that weren't found."""
        return list({get_word_from_path(path, self.__board) for path in max_score_paths(self.__board, self.__valid_words)})

    def set_randomized_board(self) -> None:
        """Sets up a new randomized board."""
        self.__board = randomize_board()

    def get_letter_list(self) -> List[str]:
        """Returns a list of letters from the board ordered by columns and rows."""
        return [letter for row in self.__board for letter in row]

    def get_cell_dict(self) -> Dict[Tuple[int, int], str]:
        """Returns a dictionary with the cells as keys and the letters as items."""
        return {(row, column): self.__board[row][column] for row in
                range(4) for column in range(4)}

    def get_start_time(self) -> int:
        """Returns the time left."""
        return self.__start_time

    def get_cell_loc(self, index: int) -> Tuple[int, int]:
        return (index // 4, index % 4)

    def get_current_word(self) -> str:
        return self.__current_word

    def reset(self) -> None:
        self.set_randomized_board()
        self.__current_word = ""
        self.__score = 0
        self.__words = []
        self.__path = []