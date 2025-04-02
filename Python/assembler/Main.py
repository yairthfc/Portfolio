"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def compute(a) -> str :
    a_temp = int(a)
    str_ = ""
    for i in range(15, -1, -1):
        b = pow(2, i)
        if b <= a_temp :
            str_ += "1"
            a_temp = a_temp - b
        else:
            str_ += "0"
    return str_




def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    # parser = Parser(input_file)
    # Note that you can write to output_file like so:
    # output_file.write("Hello world! \n")
    symboltable1 = SymbolTable()
    counter_code = 0
    first_parser = Parser(input_file)
    while first_parser.has_more_commands():
        symb = first_parser.command_type()
        if symb == "L_COMMAND":
            l = first_parser.symbol()
            symboltable1.add_entry(l, counter_code)
        else :
            counter_code += 1
        first_parser.advance()
    parser = Parser(input_file)
    symboltable__next = 16
    text = ""
    while parser.has_more_commands() :
        symb = parser.command_type()
        binary = ""
        if symb == "C_COMMAND" :
            dest = parser.dest()
            comp = parser.comp()
            jump = parser.jump()
            binatyDest = Code.dest(dest)
            binaryComp = Code.comp(comp)
            binaryJump = Code.jump(jump)
            binary = "111" + str(binaryComp) + str(binatyDest) + str(binaryJump)
        elif symb == "A_COMMAND" :
            a = parser.symbol()
            if symboltable1.contains(a) :
                address = symboltable1.get_address(a)
                binary = compute(address)
            else :
                if a.isnumeric() :
                    binary = compute(a)
                else:
                    symboltable1.add_entry(a, symboltable__next)
                    symboltable__next += 1
                    address = symboltable1.get_address(a)
                    binary = compute(address)
        elif symb == "L_COMMAND" :
            pass
        else:
            parser.advance()
            continue
        text = text + str(binary) + "\n"
        parser.advance()
    output_file.write(text)


#input_f = """// This file is part of www.nand2tetris.org \n// and the book "The Elements of Computing Systems"\n// by Nisan and Schocken, MIT Press.\n// File name: projects/06/add/Add.asm\n// Computes R0 = 2 + 3  (R0 refers to RAM[0])\n@2\nD=A\n@3\nD=D+A\n@0\nM=D"""


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
