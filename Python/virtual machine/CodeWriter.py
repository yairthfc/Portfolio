"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""
    label_count = 0
    loop_counter = 0

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        self.__output_stream = output_stream
        self.input_filename = None

        self.__output_stream.write("")

    def bootstrap_write(self):
        self.__output_stream.write("@256\n")
        self.__output_stream.write("D=A\n")
        self.__output_stream.write("@SP\n")
        self.__output_stream.write("M=D\n")

        self.write_call("Sys.init", 0)

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        self.input_filename = filename

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!
        if command == "add":
            self.if_add()
        elif command == "sub":
            self.if_sub()
        elif command == "neg":
            self.if_neg()
        elif command == "eq":
            self.if_eq_lt_gt("eq")
        elif command == "lt":
            self.if_eq_lt_gt("lt")
        elif command == "gt":
            self.if_eq_lt_gt("gt")
        elif command == "and":
            self.if_and_or("and")
        elif command == "or":
            self.if_and_or("or")
        elif command == "not":
            self.if_not()
        elif command == "shiftRight":
            self.if_shift_right()
        elif command == "shiftLeft":
            self.if_shift_left()
            #***********************ok****************************
    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        if command == "C_POP":
            self.if_pop(segment, index)
        else:
            self.if_push(segment, index)
        #***************************ok*********************************

    def close(self):
        self.__output_stream.close()

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command.
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self.__output_stream.write("(" + label + ")" + "\n")
        print(label)

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self.__output_stream.write("//goto" + label + "\n")
        self.__output_stream.write("@" + label + str(self.label_count) + "\n")
        self.__output_stream.write("0;JMP\n")


    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self.__output_stream.write("//if-goto " + label + "\n") #added self.call_counter +
        self.__output_stream.write("@SP\n")
        self.__output_stream.write("M=M-1\n")
        self.__output_stream.write("A=M\n")
        self.__output_stream.write("D=M\n")
        self.__output_stream.write("@" + label + "\n")

        self.__output_stream.write("D;JNE\n")

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command.
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0

        self.__output_stream.write("(" + function_name + str(self.label_count) + ")" + "\n") #addedself.call_counter +
        for i in range(int(n_vars)):
            self.__output_stream.write("@SP\n")
            self.__output_stream.write("A=M\n")
            self.__output_stream.write("M=0\n")
            self.SP_down_or_up("up")

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command.
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code

        CodeWriter.label_count += 1
        ret_add = function_name + "$ret." + str(CodeWriter.label_count)



          #i added this
            #*******************from here ok
        self.__output_stream.write("@" + ret_add + "\n")
        self.__output_stream.write("D=A\n")
        self.__output_stream.write("@SP\n")
        self.__output_stream.write("A=M\n")  # i added this
        self.__output_stream.write("M=D\n")
        self.SP_down_or_up("up")
        # push LCL
        self.push_val_in_sp("LCL")
        # push ARG
        self.push_val_in_sp("ARG")
        # push THIS
        self.push_val_in_sp("THIS")
        #push THAT
        self.push_val_in_sp("THAT")

        # ARG = SP-5-n_args    #ok
        self.__output_stream.write("@SP\n")
        self.__output_stream.write("D=M\n")
        num_of_diss= 5 + int(n_args)
        self.__output_stream.write("@" + str(num_of_diss) + "\n")
        self.__output_stream.write("D=D-A\n")
        self.__output_stream.write("@ARG\n")
        self.__output_stream.write("M=D\n")
        # LCL = SP
        self.__output_stream.write("@SP\n")
        self.__output_stream.write("D=M\n")
        self.__output_stream.write("@LCL\n")
        self.__output_stream.write("M=D\n")

        # goto function_name
        self.write_goto(function_name)

        #return label
        self.__output_stream.write("(" + ret_add + ")"+"\n")


    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address

        # endFrame(R15) = LCL  -> frame its ok
        self.__output_stream.write("@LCL\n")
        self.__output_stream.write("D=M\n")
        self.__output_stream.write("@R15\n")
        self.__output_stream.write("M=D\n")

        # return_address (R14) = *(frame-5) (R15-5)
        self.__output_stream.write("@5\n")
        self.__output_stream.write("D=A\n")
        self.__output_stream.write("@R15\n")
        self.__output_stream.write("D=M-D\n")
        self.__output_stream.write("A=D\n")
        self.__output_stream.write("D=M\n")
        self.__output_stream.write("@retAddr\n")
        self.__output_stream.write("M=D\n")

        # *ARG = pop() ->ok
        self.__output_stream.write("@SP\n")
        self.__output_stream.write("A=M-1\n")
        self.__output_stream.write("D=M\n")  # D contain the last argument in the stack
        self.__output_stream.write("@ARG\n")
        self.__output_stream.write("A=M\n")
        self.__output_stream.write("M=D\n")  # last argument in the stack saved in *arg

        # SP = ARG + 1  -> ok
        self.__output_stream.write("@ARG\n")
        self.__output_stream.write("D=M+1\n")
        self.__output_stream.write("@SP\n")
        self.__output_stream.write("M=D\n")
        # until here its ok***

        # THAT = *(Frame-1)
        self.framing(1, "THAT")

        # THIS = *(frame-2)
        self.framing(2, "THIS")
        # ARG = *(frame-3)
        self.framing(3, "ARG")
        # LCL = *(frame-4)
        self.framing(4, "LCL")

        # goto return_address (R15)
        self.__output_stream.write("@retAddr\n")
        self.__output_stream.write("A=M\n")
        self.__output_stream.write("0;JMP\n")

    # THIS = *(frame-2)
    def framing(self, val: int, spot: str):  # spot=This
        self.__output_stream.write("@" + str(val) + "\n")
        self.__output_stream.write("D=A\n")
        self.__output_stream.write("@R15\n")  # @endFrame
        self.__output_stream.write("D=M-D\n")  # endFrame-val
        self.__output_stream.write("A=D\n")
        self.__output_stream.write("D=M\n")
        self.__output_stream.write("@" + spot + "\n")
        self.__output_stream.write("M=D\n") #A=-5

    def SP_down_or_up(self, instruction):
        if instruction == "up":
            self.__output_stream.write("@SP\n")
            self.__output_stream.write("M=M+1\n")
        else:
            self.__output_stream.write("@SP\n")
            self.__output_stream.write("M=M-1\n")

    def if_add(self):
        self.__output_stream.write("//add\n")
        self.__output_stream.write("@SP\n")
        self.__output_stream.write("A=M-1\n")
        self.__output_stream.write("D=M\n")
        self.__output_stream.write("A=A-1\n")
        self.__output_stream.write("D=D+M\n")
        self.__output_stream.write("M=D\n")
        self.SP_down_or_up("down")

    def if_sub(self):
        self.__output_stream.write("//sub\n")
        self.__output_stream.write("@SP\n")
        self.__output_stream.write("A=M-1\n")
        self.__output_stream.write("D=M\n")
        self.__output_stream.write("A=A-1\n")
        self.__output_stream.write("M=M-D\n")
        self.SP_down_or_up("down")

    def if_neg(self):
        self.__output_stream.write("//neg\n")
        self.__output_stream.write("@SP\n")
        self.__output_stream.write("A=M-1\n")
        self.__output_stream.write("M=-M\n")

    def if_not(self):
        self.__output_stream.write("@SP\n")
        self.__output_stream.write("A=M-1\n")
        self.__output_stream.write("M=!M\n")

    def if_shift_right(self):
        self.__output_stream.write("@SP\n")
        self.__output_stream.write("A=M-1\n")
        self.__output_stream.write("M=>>M\n")

    def if_shift_left(self):
        self.__output_stream.write("@SP\n")
        self.__output_stream.write("A=M-1\n")
        self.__output_stream.write("M=<<M\n")

    def if_and_or(self, sel:str):
        self.SP_down_or_up("down")
        self.__output_stream.write("A=M\n")
        self.__output_stream.write("D=M\n")
        self.__output_stream.write("A=A-1\n")
        if sel == "and":
            self.__output_stream.write("D=D&M\n")
        else:
            self.__output_stream.write("D=D|M\n")
        self.__output_stream.write("M=D\n")

    def make_add(self, segmant, index):
        if segmant in ["local", "argument", "this", "that"]:
            if segmant == "local":
                segmant = "LCL"
            elif segmant == "argument":
                segmant = "ARG"
            elif segmant == "this":
                segmant = "THIS"
            else:
                segmant = "THAT"

            self.__output_stream.write("@" + index + "\n")
            self.__output_stream.write("D=A\n")
            self.__output_stream.write("@" + segmant + "\n")
            self.__output_stream.write("D=D+M\n")
            self.__output_stream.write("@R13\n")
            self.__output_stream.write("M=D\n")
        elif segmant == "temp":
            index = str(int(index) + 5)
            if int(index) > 12:
                raise "problem detected"
            self.__output_stream.write("@" + index + "\n")
            self.__output_stream.write("D=A\n")
            self.__output_stream.write("@R13\n")
            self.__output_stream.write("M=D\n")
        elif segmant == "static":

             ind = str(int(index))
             if int(ind) > 240:
                 raise "problem detected"
             self.__output_stream.write("@" +  self.input_filename + "." + ind + "\n")
             self.__output_stream.write("D=A\n")
             self.__output_stream.write("@R13\n")
             self.__output_stream.write("M=D\n")

    def if_pop(self, segmant, index): #pop
        self.__output_stream.write("//pop " + segmant + " " + index +"\n")

        self.SP_down_or_up("down\n")
        if segmant == "pointer":
            self.__output_stream.write("A=M\n")
            self.__output_stream.write("D=M\n")
            if int(index) == 0:

                self.__output_stream.write("@THIS\n")
            else:
                self.__output_stream.write("@THAT\n")

            self.__output_stream.write("M=D\n")


        else:
            self.make_add(segmant, index)
            self.__output_stream.write("@SP\n")
            self.__output_stream.write("A=M\n")
            self.__output_stream.write("D=M\n")  #D = the value to pop
            self.__output_stream.write("@R13\n")
            self.__output_stream.write("A=M\n")
            self.__output_stream.write("M=D\n")  #until here ok

    def if_push(self, segmant, index):
        self.__output_stream.write("//push " + segmant + " " + index +"\n")
        if segmant == "constant" :
            self.push_constant(index)  #ok
        elif segmant == "pointer":    #this=3, that=4
            if int(index) == 0:
                self.__output_stream.write("@THIS\n")  #change this to 3
            else:
                self.__output_stream.write("@THAT\n")    #changed this to 4
            self.__output_stream.write("D=M\n")
            self.__output_stream.write("@SP\n")
            self.__output_stream.write("A=M\n")
            self.__output_stream.write("M=D\n")
            self.SP_down_or_up("up")

        else:  #no static and no pointer

            self.make_add(segmant, index)
            self.__output_stream.write("@R13\n")
            self.__output_stream.write("A=M\n") #added this line
            self.__output_stream.write("D=M\n")
            self.__output_stream.write("@SP\n")
            self.__output_stream.write("A=M\n")
            self.__output_stream.write("M=D\n")
            self.SP_down_or_up("up")

    def push_constant(self, index):  #---------------------->ok
        self.__output_stream.write("@" + index + "\n")
        self.__output_stream.write("D=A\n")
        self.__output_stream.write("@SP\n")
        self.__output_stream.write("A=M\n")
        self.__output_stream.write("M=D\n")
        self.SP_down_or_up("up")

    def if_eq_lt_gt(self, cond:str):
        # SP down
        self.SP_down_or_up("down")

        # A=M
        self.__output_stream.write("A=M\n")

        # D=M
        self.__output_stream.write("D=M\n")

        # Check conditions and jump accordingly
        self.__output_stream.write("@Ypos" + "." + str(self.loop_counter) + str(CodeWriter.label_count) + "\n")
        self.__output_stream.write("D;JGE\n")

        # spdown()
        self.SP_down_or_up("down")

        # A=M
        self.__output_stream.write("A=M\n")

        # D=M
        self.__output_stream.write("D=M\n")

        # Check conditions and jump accordingly
        self.__output_stream.write("@XposYneg" + "." + str(self.loop_counter)+ str(CodeWriter.label_count) + "\n")
        self.__output_stream.write("D;JGE\n")

        # A=A+1
        self.__output_stream.write("A=A+1\n")

        # D=M-D
        self.__output_stream.write("D=M-D\n")

        # @END_TEMP
        self.__output_stream.write("@END_TEMP" + "." + str(self.loop_counter) + str(CodeWriter.label_count) + "\n")
        self.__output_stream.write("0;JMP\n")

        # (XposYneg)
        self.__output_stream.write("(XposYneg" + "." + str(self.loop_counter) + str(CodeWriter.label_count) + ")\n")
        self.__output_stream.write("D=-1\n")
        self.__output_stream.write("@END_TEMP" + "." + str(self.loop_counter) + str(CodeWriter.label_count) + "\n")
        self.__output_stream.write("0;JMP\n")

        self.__output_stream.write("(Ypos"+ "." + str(self.loop_counter) + str(CodeWriter.label_count) + ")\n")
        self.SP_down_or_up("down")
        self.__output_stream.write("A=M\n")
        self.__output_stream.write("D=M\n")
        self.__output_stream.write("@YposXpos" + "." + str(self.loop_counter)+ str(CodeWriter.label_count) + "\n")
        self.__output_stream.write("D;JGE\n")
        self.__output_stream.write("D=1\n")
        self.__output_stream.write("@END_TEMP" + "." + str(self.loop_counter)+ str(CodeWriter.label_count) + "\n")
        self.__output_stream.write("0;JMP\n")

        # (YposXpos)
        self.__output_stream.write("(YposXpos" + "." + str(self.loop_counter) + str(CodeWriter.label_count) + ")\n")
        self.__output_stream.write("@SP\n")
        self.__output_stream.write("A=M+1\n")
        self.__output_stream.write("D=M-D\n")
        self.__output_stream.write("@END_TEMP" + "." + str(self.loop_counter) + str(CodeWriter.label_count) + "\n")
        self.__output_stream.write("0;JMP\n")

        # (END_TEMP)
        self.__output_stream.write("(END_TEMP" + "." + str(self.loop_counter)+ str(CodeWriter.label_count) + ")\n")


        self.__output_stream.write("@TRUELABEL" + "." + str(self.loop_counter) + str(CodeWriter.label_count) + "\n")
        if cond == "eq":
            self.__output_stream.write("D;JEQ\n")
        elif cond == "lt":
            self.__output_stream.write("D;JGT\n")
        else:
            self.__output_stream.write("D;JLT\n")
        self.__output_stream.write("D=0\n")
        self.__output_stream.write("@END" + str(CodeWriter.label_count) + "\n")
        self.__output_stream.write("0;JMP\n")
        self.__output_stream.write("(TRUELABEL" + "." + str(self.loop_counter)+ str(CodeWriter.label_count) + ")\n")
        self.__output_stream.write("D=-1\n")
        self.__output_stream.write("(END" + str(CodeWriter.label_count) + ")\n")
        self.__output_stream.write("@SP\n")
        self.__output_stream.write("A=M\n")
        self.__output_stream.write("M=D\n")
        self.SP_down_or_up("up")
        self.loop_counter+= 1



    def push_val_in_sp(self, val: str):
        self.__output_stream.write("@" + val + "\n")
        self.__output_stream.write("D=M\n")
        self.__output_stream.write("@SP\n")
        self.__output_stream.write("A=M\n")  #i added this
        self.__output_stream.write("M=D\n")
        self.SP_down_or_up("up")