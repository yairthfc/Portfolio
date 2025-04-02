"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        self.__input_lines = input_file.read().splitlines()
        self.__counter = 0
        self.__end = len(self.__input_lines)
        self.__cur_line = self.__input_lines[0]


    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        if self.__counter >= self.__end:
            return False
        else:
            return True

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        # Your code goes here!
        self.__counter = self.__counter + 1
        if self.has_more_commands():
            print(self.__counter)
            self.__cur_line = self.__input_lines[self.__counter]
            
        else:
            
            pass

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        # Your code goes here!
        if self.__cur_line == "" :
            return "null"
        while self.__cur_line[0] == " " :
            self.__cur_line = self.__cur_line[1:]
        if self.__cur_line[0] == "@":
            return "A_COMMAND"
        elif self.__cur_line[0] == "(":
            return "L_COMMAND"
        elif self.__cur_line[0] == "/" :
            return "null"
        else:
            return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        # Your code goes here!

        com = self.command_type()
        list = self.__cur_line.split(" ")
        cur_line = list[0]
        if com == "A_COMMAND" :
            return cur_line[1:]
        if com == "L_COMMAND" :
            return cur_line[1:-1]


    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        com = self.command_type()
        if com != "null" :
            list = self.__cur_line.split(" ")
            cur_line = list[0]
            if com == "C_COMMAND" :
                ind_eq = cur_line.find("=")
                ind_ot = cur_line.find(";")
                if ind_eq != -1 :
                    return cur_line[:ind_eq]
                else:
                    return "null"

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        list = self.__cur_line.split(" ")
        cur_line = list[0]
        ind_eq = cur_line.find("=")
        ind_ot = cur_line.find(";")
        if ind_eq != -1 :
            if ind_ot != -1 :
                return cur_line[ind_eq+ 1:ind_ot]
            else:
                return cur_line[ind_eq+1:]
        else:
            return cur_line[:ind_ot]

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        com = self.command_type()
        if com != "null" :
            list = self.__cur_line.split(" ")
            cur_line = list[0]
            if com == "C_COMMAND" :
                ind_eq = cur_line.find("=")
                ind_ot = cur_line.find(";")
                if ind_ot != -1 :
                    return cur_line[ind_ot+ 1:]
                else:
                    return "null"








