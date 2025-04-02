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
from Parser import Parser
from CodeWriter import CodeWriter


def translate_file( input_file: typing.TextIO, output_file: typing.TextIO,bootstrap: bool) -> None:
    """Translates a single file.

    Args:
        input_file (typing.TextIO): the file to translate.
        output_file (typing.TextIO): writes all output to this file.
        bootstrap (bool): if this is True, the current file is the
            first file we are translating.
    """
    # Your code goes here!
    code_writer = CodeWriter(output_file)

    parser = Parser(input_file)
    input_filename = os.path.splitext(os.path.basename(input_file.name))[0]
    code_writer.set_file_name(input_filename)
    if bootstrap:
         code_writer.bootstrap_write()
    functionName = input_filename + "." + "Sys"

    while parser.has_more_commands():
        type = parser.command_type()  #get the command type
        if type == "C_ARITHMETIC":
            sub_type = parser.arg1()
            code_writer.write_arithmetic(sub_type)
        elif type == "C_PUSH":
                #write if its push
            arg1 = parser.arg1()
            arg2 = parser.arg2()
            code_writer.write_push_pop("C_PUSH", arg1, arg2)
        elif type == "C_POP":
                #write if its pop
            arg1 = parser.arg1()
            arg2 = parser.arg2()
            code_writer.write_push_pop("C_POP", arg1, arg2)
        elif type == "C_GOTO":
            arg1 = functionName + ".$." + parser.arg1() ##added this
            code_writer.write_goto(arg1)
        elif type == "C_IF":
            arg1 = functionName + ".$." + parser.arg1() ##added this
            code_writer.write_if(arg1)
        elif type == "C_LABEL":
            arg1 = functionName + ".$." + parser.arg1() ##added this
            code_writer.write_label(arg1)
        elif type == "C_CALL":
            arg1 = parser.arg1()
            arg2 = parser.arg2()
            functionName =   arg1
            code_writer.write_call(arg1, arg2)
        elif type == "C_FUNCTION":
            arg1 = parser.arg1()
            functionName =  arg1
            arg2 = parser.arg2()
            code_writer.write_function(arg1, arg2)
        elif type == "C_RETURN":
            code_writer.write_return()
        parser.advance()


if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(argument_path))

    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    bootstrap = True
    with open(output_path, 'w') as output_file:
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                translate_file(input_file, output_file, bootstrap)
            bootstrap = False

