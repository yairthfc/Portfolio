"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from VMWriter import VMWriter
from SymbolTable import SymbolTable

class CompilationEngine:
    """Gets input from a self.input and emits its parsed structure into an
    output stream.
    """
    method_type = ["var","argument","field","static"]
    statements = ["if", "do", "while", "return", "let"]
    ops = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
    unary_ops = ['-', '~']
    arithmetics = ['-', '/', '+', '*']

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """

        self.class_name = None
        self.vm_writer = VMWriter(output_stream)
        self.symbolTable = SymbolTable()
        self.output_stream = output_stream
        self.input = input_stream
        self.l_counter = 0
        self.unary_op = ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=']

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.class_name = self.input.tokens[1]

        # pass 'class nameClass {'
        self.input.advance(3)
        # declare class's vars:
        while self.input.keyword().lower() in ["static", "field"]:
            self.compile_class_var_dec()
        while self.input.cur_token in ["constructor", "function", "method"]:
            self.compile_subroutine()

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        kind = self.input.cur_token
        self.input.advance(1)
        type = self.input.cur_token
        self.input.advance(1)
        name = self.input.cur_token
        self.input.advance(1)
        self.symbolTable.define(name, type, kind)
        self.vm_writer.write_push(kind, self.symbolTable.index_of(name))

        while self.input.cur_token == ',':
            self.input.advance(1)
            name = self.input.cur_token
            self.input.advance(1)
            self.symbolTable.define(name, type, kind)
            self.vm_writer.write_push(kind, self.symbolTable.index_of(name))
        self.input.advance(1)

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.symbolTable.start_subroutine()
        kind_of_sub = self.input.cur_token
        self.input.advance(1)
        return_type = self.input.cur_token  # maybe I can delete this
        self.input.advance(1)
        name_sub = self.input.cur_token
        self.input.advance(2)
        count_param = self.compile_parameter_list()
        self.input.advance(2)  # ) + {
        self.output_stream.write("function " + self.class_name + "." + name_sub + " " + str(count_param) + "\n")
        if kind_of_sub == "method":
            self.symbolTable.define("this", self.class_name, "argument")
            self.vm_writer.write_push('argument', 0)
            self.vm_writer.write_pop('pointer', 0)

        if kind_of_sub == 'constructor':
            field_count = self.symbolTable.var_count("field")
            self.vm_writer.write_push('constant', field_count)
            self.vm_writer.write_call('Memory.alloc', 1)
            self.vm_writer.write_pop('pointer', 0)

        self.compile_subroutine_body()
        self.input.advance(1)  # skip }

    def compile_subroutine_body(self):

        while self.input.symbol() != "}":
            self.compile_var_dec()
            self.compile_statements()

        return

    def compile_parameter_list(self) -> int:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        count = 0
        while self.input.cur_token != ")":
            if (self.input.cur_token == ','):
                self.input.advance(1)
            type_parameter = self.input.cur_token
            self.input.advance(1)
            name_parameter = self.input.cur_token
            self.input.advance(1)
            self.symbolTable.define(name_parameter, type_parameter, "argument")
            count += 1
        return count

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""

        while self.input.cur_token in self.method_type:

            kind = self.input.cur_token
            self.input.advance(1)
            type = self.input.cur_token
            self.input.advance(1)
            name = self.input.cur_token
            self.input.advance(1)
            self.symbolTable.define(name, type, kind)
            self.vm_writer.write_push(kind , self.symbolTable.index_of(name))
            while self.input.cur_token != ';':
                self.input.advance(1)  # skip ','
                name = self.input.cur_token
                self.input.advance(1) #skip name
                self.symbolTable.define(name, type, kind)
                self.vm_writer.write_push(kind, self.symbolTable.index_of(name))
            self.input.advance(1)  #skip ;

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """

        while self.input.cur_token in self.statements:  # ;

            if self.input.cur_token == "let":
                self.compile_let()
            elif self.input.cur_token == "if":
                self.compile_if()
            elif self.input.cur_token == "while":
                self.compile_while()
            elif self.input.cur_token == "do":
                self.compile_do()
            elif self.input.cur_token == "return":
                self.compile_return()

    def compile_let(self) -> None:
        """Compiles a let statement."""
        is_array = False
        self.input.advance(1) # skip 'let'

        obj_name = self.input.cur_token
        obj_type = self.symbolTable.type_of(obj_name)
        obj_index = self.symbolTable.index_of(obj_name)

        self.input.advance(1)  # skip 'name'
        if self.input.cur_token == "[":
            is_array = True
            self.input.advance(1) # skip [
            self.compile_expression()
            self.input.advance(1)  # skip ]
            self.vm_writer.write_push(obj_type, obj_index)
            self.vm_writer.write_arithmetic("ADD")
        self.input.advance(1)  # skip '='
        self.compile_expression()
        if is_array:
            self.vm_writer.write_pop("TEMP", 0)
            self.vm_writer.write_pop("POINTER", 1)
            self.vm_writer.write_push("TEMP", 0)
            self.vm_writer.write_pop("THAT", 0)
        else:
            self.vm_writer.write_pop(obj_type, obj_index)
        self.input.advance(1)

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Initialize labels
        l_while = "WHILE_LABEL" + str(self.l_counter)
        l_end = "END_WHILE" + str(self.l_counter)
        self.l_counter += 1

        self.vm_writer.write_label(l_while)
        self.input.advance(2)   # skip 'while' and '('

        self.compile_expression()

        self.input.advance(2)   # skip ')' and '{'
        self.vm_writer.write_arithmetic("NOT")
        self.vm_writer.write_if_go_to(l_end)
        self.compile_statements()

        self.vm_writer.write_goto(l_while)
        self.input.advance(1)  # skip '}'

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!

        self.input.advance(1) # skip return
        if self.input.cur_token != ";":
            self.compile_expression()
        self.input.advance(1)

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # initial labels
        l_false = 'IF_FALSE' + str(self.l_counter)
        l_end = 'END_IF' + str(self.l_counter)
        self.l_counter += 1

        self.input.advance(2)  # skip if and (
        self.compile_expression()
        self.input.advance(2)  # skip ) and {
        self.vm_writer.write_arithmetic("NOT")
        self.vm_writer.write_if_go_to(l_false)
        # if true
        self.compile_statements()
        self.vm_writer.write_goto(l_end)
        self.input.advance(1)  # skip }
        # if false
        self.vm_writer.write_label(l_false)
        if self.input.cur_token == "else":
            self.input.advance(1)  # skip "else
            self.compile_statements()
            self.input.advance(1)
        self.vm_writer.write_label(l_end)  # end if

    def compile_expression(self) -> None:
        """Compiles an expression."""

        self.compile_term()
        while self.input.token_type() == "SYMBOL" and self.input.cur_token in self.ops:
            operator = self.input.cur_token
            self.input.advance(1)
            self.compile_term()
            if operator == "*":
                self.vm_writer.write_call("Math.multiply", 2)
            elif operator == "/":
                self.vm_writer.write_call("Math.divide", 2)
            else:
                self.vm_writer.write_arithmetic(operator)

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """

        if self.input.token_type() == "INT_CONST":
            self.vm_writer.write_push("constant", self.input.cur_token)
            self.input.advance(1)

        elif self.input.token_type() == "STRING_CONST":
            self.get_string()


        elif self.input.token_type() == "KEYWORD":
            if self.input.cur_token == 'true' or 'false' or 'null':
                self.vm_writer.write_push("constant", 0)
                if self.input.cur_token == "true":
                    self.vm_writer.write_push("constant", -1)
                self.input.advance(1)
            elif self.input.cur_token == "this":
                self.input.advance(1)
                self.writer.write_push("pointer", 0)

        elif self.input.token_type() == "SYMBOL":
            if self.input.symbol() == '(':
                self.input.advance(1)
                self.compile_expression()
                self.input.advance(1)

            elif self.input.cur_token in ['-', '~']:
                symbol_token = self.input.cur_token
                self.input.advance(1)
                self.compile_expression()
                if symbol_token == '-':
                    self.vm_writer.write_arithmetic("NEG")
                elif symbol_token == '~':
                    self.vm_writer.write_arithmetic("NOT")

        elif self.input.token_type() == "IDENTIFIER":
            self.handle_identifier()

    def get_string(self)->None:
        string = self.input.cur_token[1:-1]
        self.input.advance(1)
        self.vm_writer.write_push("constant", len(string))
        self.vm_writer.write_call("String.new", 1)

        for char in string:
            self.vm_writer.write_push("constant", ord(char))
            self.vm_writer.write_call("String.appendChar", 2)

    def handle_identifier(self)-> None:
        name = self.input.cur_token
        type = self.symbolTable.type_of(name)
        index = self.symbolTable.index_of(name)
        self.vm_writer.write_push(type, index)
        self.input.advance(1)

        if self.input.token_type() != "SYMBOL":
            pass
        else:
            if self.input.symbol() == '(' or self.input.symbol() == '.':
                self.compile_subroutine_call()
            elif self.input.symbol() == '[':  # array
                self.input.advance(1)  # skip [
                self.compile_expression()
                self.input.advance(1)  # skip ]
                self.vm_writer.write_push(type, name)
                self.vm_writer.write_arithmetic("ADD")
                self.vm_writer.write_pop("pointer", 1)
                self.vm_writer.write_push("that", 0)

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        if self.input.symbol() != ")":
            self.compile_expression()
            while self.input.symbol() == ",":
                self.write_wrap()
                self.input.advance(0)
                self.compile_expression()
        else:
            pass

    def write_wrap(self):
        return

    def compile_subroutine_call(self):
        if self.input.symbol() == '(':
            self.write_wrap()  # (
            self.input.advance(1)
            self.compile_expression_list()
            self.write_wrap()
            self.input.advance(1)
        elif self.input.symbol() == '.':

            self.write_wrap()
            self.input.advance(1)
            self.write_wrap()
            self.input.advance(1)
            self.write_wrap()
            self.input.advance(1)
            self.compile_expression_list()
            self.write_wrap()
            self.input.advance(1)

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
       
        self.write_wrap()  # do
        self.input.advance(3)
        self.write_wrap()

        self.compile_subroutine_call()
        self.write_wrap()  # ;
        self.input.advance(1)

