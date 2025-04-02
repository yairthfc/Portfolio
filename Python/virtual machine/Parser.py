"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """
    # Parser
    
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.

    ## VM Language Specification

    A .vm file is a stream of characters. If the file represents a
    valid program, it can be translated into a stream of valid assembly 
    commands. VM commands may be separated by an arbitrary number of whitespace
    characters and comments, which are ignored. Comments begin with "//" and
    last until the line’s end.
    The different parts of each VM command may also be separated by an arbitrary
    number of non-newline whitespace characters.

    - Arithmetic commands:
      - add, sub, and, or, eq, gt, lt
      - neg, not, shiftleft, shiftright
    - Memory segment manipulation:
      - push <segment> <number>
      - pop <segment that is not constant> <number>
      - <segment> can be any of: argument, local, static, constant, this, that, 
                                 pointer, temp
    - Branching (only relevant for project 8):
      - label <label-name>
      - if-goto <label-name>
      - goto <label-name>
      - <label-name> can be any combination of non-whitespace characters.
    - Functions (only relevant for project 8):
      - call <function-name> <n-args>
      - function <function-name> <n-vars>
      - return
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        self.__input_lines = input_file.read().splitlines()
        self.__counter = 0
        self.__num_of_lines = len(self.__input_lines)
        self.__cur_line = self.__input_lines[0]


        

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        if self.__counter >= self.__num_of_lines:
            return False
        else:
            return True

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        # Your code goes here!
        self.__counter = self.__counter + 1
        if self.has_more_commands():
            self.__cur_line = self.__input_lines[self.__counter]
        else:
            pass

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        # Your code goes here!
        #checks if its empty
        if self.__cur_line == "":
            return "null"
        elif self.__cur_line[0] == "/":
            return "null"
        #cuts the first spaces
        while self.__cur_line[0] == " ":
            self.__cur_line = self.__cur_line[1:]
        # checks if it arithmetic

        if self.__cur_line.startswith(("add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not", "shiftLeft",
                                       "shiftRight")):
            return "C_ARITHMETIC"
        #checks if pop
        elif self.__cur_line.startswith("pop"):
            return "C_POP"
        # checks if push
        elif self.__cur_line.startswith("push") :
            return "C_PUSH"
        elif self.__cur_line.startswith("label"):
            return "C_LABEL"
        elif self.__cur_line.startswith("goto"):
            return "C_GOTO"
        elif self.__cur_line.startswith("if-goto"):
            return "C_IF"
        elif self.__cur_line.startswith("call"):
            return "C_CALL"
        elif self.__cur_line.startswith("function"):
            return "C_FUNCTION"
        elif self.__cur_line.startswith("return"):
            return "C_RETURN"
        

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        # Your code goes here!
        #if arithmetic
        if self.command_type() == "C_ARITHMETIC" :
            return self.__cur_line.split()[0]
        # if not 
        elif self.command_type() == "C_RETURN":
            pass
        else :
            list = self.__cur_line.split(" ")
            return list[1]

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        # Your code goes here!
        if self.command_type() in ["C_PUSH", "C_POP","C_FUNCTION", "C_CALL"] :
            list = self.__cur_line.split(" ")
            return list[2]
        else:
            pass