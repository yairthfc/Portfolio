#################################################################
# FILE : ex11_utils.py
# WRITERS : David Zvi Kadish (davidzvi), Yair Mahfud (yairthfc)
# EXERCISE : intro2cs1 ex11 2023
# DESCRIPTION: Uselful functions for the game.
# WEBSITES I USED: www.w3schools.com, www.programiz.com
#################################################################

from typing import List, Tuple, Iterable, Optional, Set, Dict
import time
from boggle_board_randomizer import randomize_board

Board = List[List[str]]
Path = List[Tuple[int, int]]
Location = Tuple[int, int]
# The valid directions for the next letter to be chosen after the previous one -
# we can check if we get one of these tuples by subtracting the next letter's
# coordinates from the previous one's and checking if the result is one of the
# tuples in the list.
VALID_DIRECTIONS = [(i, j) for i in range(-1, 2)
                    for j in range(-1, 2) if (i, j) != (0, 0)]
BOARD_LOCATIONS = [(i, j) for i in range(4) for j in range(4)]
GAME_OVER_TEXT: str = "Game Over!\nTo play again press Start Game.\n"
MAX_SCORE_TEXT: str = "Highest Score Possible from this\nboard: "
UNFOUND_WORDS_TEXT: str = "Words you didn't find:\n"


def loc_in_board(loc: Location) -> bool:
    """Checks if a location is on the board."""
    return loc in BOARD_LOCATIONS


def valid_move(origin: Location, destination: Location) -> bool:
    """Checks if it's legal to 'move' from the original location to the
       destination during following a path."""
    return (destination[0] - origin[0], destination[1] - origin[1]) in VALID_DIRECTIONS


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    """Checks is a given path is valid. If it is and the word resulting connecting
       the letters in the path is in the dictionary the function will return the
       word, and None otherwise."""
    if path == [] or list(words) == []:
        return None
    word_set: Set[str] = get_length_until_n_words(
        list(words), find_longest_word_length(list(words)))
    if not loc_in_board((path[0][0], path[0][1])) or \
            board[path[0][0]][path[0][1]] not in word_set:
        return None
    word = board[path[0][0]][path[0][1]]
    path_locs = [(path[0][0], path[0][1])]
    for index, loc in enumerate(path[1:], start=1):
        if not valid_move(path[index - 1], loc) or not loc_in_board(loc) or loc \
                in path_locs or word not in word_set:
            return None
        word += board[path[index][0]][path[index][1]]
        path_locs.append(loc)
    return word


def get_valid_directions_for_cell(loc: Location) -> List[Location]:
    """Returns a list of all directions that point at a cell on the board for the given cell."""
    return [direction for direction in VALID_DIRECTIONS if (
        loc[0] + direction[0], loc[1] + direction[1]) in BOARD_LOCATIONS]


def get_filtered_direcrtions_for_cell(loc: Location, path: Path) -> Iterable[Location]:
    """Returns an iterable of all directions the location can point at that
       aren't in the path."""
    return filter(lambda direction: (loc[0] + direction[0], loc[1] + direction[1]) not in path,
                  get_valid_directions_for_cell(loc))


def get_length_until_n_words(words: List[str], n: int) -> Set[str]:
    """Returns a set of all words that can be made out of words in the word list
       of length of up to n characters."""
    return {word[:index] for word in words for index in range(1, n + 1) if len(word) <= n}


def get_letters_around_cell(loc: Location, board: Board) -> Set[str]:
    """Returns a set of all locations around the the given location."""
    return {board[loc[0] + direction[0]][loc[1] + direction[1]] for direction
            in VALID_DIRECTIONS if loc_in_board((loc[0] + direction[0], loc[1] + direction[1]))}


def word_continues(word: str, word_set: Set[str], letter_set: Set[str]) -> bool:
    """Checks if the current word has a continuation in the word set."""
    return any(list(map(lambda l: word + l in word_set, letter_set)))


def generate_length_n_paths(n: int, board: Board, word_set: Set[str],
                            words: List[str], paths: List[Path] = [],
                            word: str = "", path: Path = []) -> None:
    """Fills a given empty list with all valid paths of length n that represent
       valid words."""
    if len(path) == n:
        if word in words:
            paths.append(path)
        return
    elif path == []:
        for row in range(4):
            for col in range(4):
                next_loc = row, col
                generate_length_n_paths(n, board, word_set, words, paths, word + board[
                    next_loc[0]][next_loc[1]], path + [next_loc])
    elif word not in word_set:
        return
    else:
        current_loc = path[-1]
        for direction in get_filtered_direcrtions_for_cell(current_loc, path):
            next_loc = current_loc[0] + \
                direction[0], current_loc[1] + direction[1]
            # If the current "beginning" of the word doesn't exist in the word
            # set there's no point to keep checking if the next valid letters
            # after the current word will complete it into a valid word.
            if not word_continues(word, word_set, get_letters_around_cell(current_loc, board)):
                return
            generate_length_n_paths(n, board, word_set, words, paths, word + board[
                next_loc[0]][next_loc[1]], path + [next_loc])


def find_longest_word_length(words: List[str]) -> int:
    """Returns the length of the longest word in the given word list."""
    return len(max(words, key=lambda word: len(word)))


def find_shortest_word_length(words: List[str]) -> int:
    """Returns the length of the shortest word in the given word list."""
    return len(min(words, key=lambda word: len(word)))


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """Finds all paths of length n that represent valid words in the word iterable."""
    paths: List[Path] = []
    word_set = get_length_until_n_words(list(words),
                                        find_longest_word_length(list(words)))
    generate_length_n_paths(n, board, word_set, list(words), paths)
    return paths


def generate_length_n_words(n: int, board: Board, word_set: Set[str],
                            words: List[str], paths: List[Path] = [],
                            word: str = "", path: Path = []) -> None:
    """Fills a given empty list with all valid paths that represent valid words
       of length n."""
    if len(word) > n:
        return
    elif len(word) == n:
        if word in words:
            paths.append(path)
        return
    elif path == []:
        for row in range(4):
            for col in range(4):
                next_loc = row, col
                generate_length_n_words(n, board, word_set, words, paths, word +
                                        board[next_loc[0]][next_loc[1]], path + [next_loc])
    elif word not in word_set:
        return
    else:
        current_loc = path[-1]
        for direction in get_filtered_direcrtions_for_cell(current_loc, path):
            next_loc = current_loc[0] + \
                direction[0], current_loc[1] + direction[1]
            # If the current "beginning" of the word doesn't exist in the word
            # set there's no point to keep checking if the next valid letters
            # after the current word will complete it into a valid word.
            if not word_continues(word, word_set, get_letters_around_cell(current_loc, board)):
                return
            generate_length_n_words(n, board, word_set, words, paths, word + board[
                next_loc[0]][next_loc[1]], path + [next_loc])


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    paths: List[Path] = []
    word_set = get_length_until_n_words(list(words), n)
    generate_length_n_words(n, board, word_set, list(words), paths)
    return paths


def get_word_from_path(path: Path, board: Board) -> str:
    """Returns the word represented by a given path."""
    word = ""
    for loc in path:
        word += board[loc[0]][loc[1]]
    return word


def find_paths_for_max_score(board: Board, word_set: Set[str], words: Iterable[str],
                             word_path_dict: Dict[str, Path] = {},
                             word: str = "", path: Path = []) -> None:
    """Finds the paths that will return the max score for all valid words on the
       board."""
    if word in words:
        if word not in word_path_dict or len(path) > len(word_path_dict[word]):
            word_path_dict[word] = path
    if path == []:
        for row in range(4):
            for col in range(4):
                next_loc = row, col
                find_paths_for_max_score(board, word_set, words, word_path_dict, word +
                                         board[next_loc[0]][next_loc[1]], path + [next_loc])
    elif word not in word_set:
        return
    else:
        current_loc = path[-1]
        for direction in get_filtered_direcrtions_for_cell(current_loc, path):
            next_loc = current_loc[0] + \
                direction[0], current_loc[1] + direction[1]
            # If the current "beginning" of the word doesn't exist in the word
            # set there's no point to keep checking if the next valid letters
            # after the current word will complete it into a valid word.
            if not word_continues(word, word_set, get_letters_around_cell(current_loc, board)):
                return
            find_paths_for_max_score(board, word_set, words, word_path_dict, word +
                                     board[next_loc[0]][next_loc[1]], path + [next_loc])


def get_word_set_for_max_score(words: Iterable[str]) -> Set[str]:
    """Returns a set of word slices to help finding the max score."""
    return get_length_until_n_words(list(words), find_longest_word_length(list(words)))


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """Returns a list of paths that will get the most points in a game with the
       given words."""
    word_path_dict: Dict[str, Path] = {}
    find_paths_for_max_score(board, get_word_set_for_max_score(words), words,
                             word_path_dict)
    return list(word_path_dict.values())


def format_words(words: List[str]) -> str:
    """Formats a list of words in a way that they fit in the word display."""
    rows = 1
    word_str = ""
    for index in range(len(words)):
        if len(word_str + words[index]) > 25 * rows:
            word_str += "\n"
            rows += 1
        word_str += f"{words[index]},"
    return word_str.strip(",")


def game_over_text(unfound_words: List[int], max_score: int, found: int, all: int):
    """Returns text for the game to display when the game ends."""
    return GAME_OVER_TEXT + MAX_SCORE_TEXT + f"{max_score}\nYou found {found} out of {all} words.\n" + UNFOUND_WORDS_TEXT + format_words(unfound_words)


if __name__ == "__main__":
    with open("C:\\Users\\dzk34\\Desktop\\intro2cs\\ex11\\intro2cs_ex11\\boggle_dict.txt") as f:
        words = [word.strip("\n") for word in f]
    board = [['B', 'V', 'O', 'E'],
             ['T', 'A', 'L', 'H'],
             ['U', 'D', 'T', 'A'],
             ['Y', 'N', 'T', 'I']]
    wordso = ['TAB', 'TAIT']
    longest = find_longest_word_length(list(words))
    shortest = find_shortest_word_length(list(words))
    wordso = list({get_word_from_path(path, board) for length in range(longest, shortest - 1, -1) for path in find_length_n_words(
        length, board, words) if get_word_from_path(path, board) not in wordso})
    print(wordso)