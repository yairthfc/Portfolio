"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing




class CompilationEngine:
    check = 0
    """Gets input from a self.input and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        self.output_stream = output_stream
        self.input = input_stream
        self.unary_op = ['+' , '-' , '*' , '/' , '&amp;' , '|' , '&lt;' , '&gt;' , '=']

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!

        is_it_var = True
        is_it_sub = True
        self.write_opening_tag("class")
        self.write_wrap() #class
        self.input.advance()
        self.write_wrap() #name of class
        self.input.advance()
        self.write_wrap() #{
        self.input.advance()
        if self.input.token_type() == "KEYWORD":
            while is_it_var:
                if self.input.keyword().lower() in ["static", "field"]:
                    self.compile_class_var_dec()
                else:
                    is_it_var = False

        if self.input.token_type() == "KEYWORD":
            while is_it_sub :
                if self.input.keyword().lower() in ["constructor", "function", "method"]:
                    self.compile_subroutine()
                else:
                    is_it_sub = False
        self.write_wrap() # } - close the class
        self.input.advance()
        self.write_closing_tag("class")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        self.write_opening_tag("classVarDec")
        more_var = True
        self.write_wrap() #static/field
        self.input.advance()
        self.write_wrap() # type ver
        self.input.advance()
        self.write_wrap() #var name
        self.input.advance()
        while more_var:
            if self.input.symbol() == ",":
                self.write_wrap()  # ","
                self.input.advance()
                self.write_wrap()   #var name
                self.input.advance()
            elif self.input.symbol() == ";":
                self.write_wrap()  #";"
                self.input.advance()
                more_var = False
        self.write_closing_tag("classVarDec")

    def write_opening_tag(self, val: str):
        self.output_stream.write("<" + val + ">\n")

    def write_closing_tag(self, val: str):
        self.output_stream.write("</" + val + ">\n")
        

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        self.write_opening_tag("subroutineDec")
        self.write_wrap()  # (constructor|method|function)
        self.input.advance()
        self.write_wrap()   # (void|type)
        self.input.advance()
        self.write_wrap()   # (subroutine name)
        self.input.advance()
        self.write_wrap()  # (
        self.input.advance()
        self.compile_parameter_list()
        self.write_wrap() # )
        self.input.advance()
        #until here looks ok

        self.compile_subroutine_body()
        self.write_closing_tag("subroutineDec")

    def compile_subroutine_body(self):
        self.write_opening_tag("subroutineBody")
        self.write_wrap()  # open {
        self.input.advance()

        while self.input.symbol() != "}":
            flag = self.compile_var_dec()
            if not flag:
                self.compile_statements()

        self.write_wrap()     # close }
        self.input.advance()
        self.write_closing_tag("subroutineBody")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        self.write_opening_tag("parameterList")
        if self.input.token_type() == "SYMBOL":
            self.write_closing_tag("parameterList")
            return

        self.write_wrap()   #type of the parameter
        self.input.advance()
        self.write_wrap()   #name of the paramener
        self.input.advance()
        while self.input.symbol() == ',':
            self.write_wrap()     # ","
            self.input.advance()
            self.write_wrap()     #type of the parameter
            self.input.advance()
            self.write_wrap()     #name of the parameter
            self.input.advance()
        self.write_closing_tag("parameterList")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!

        if self.input.token_type() == "KEYWORD":
            if self.input.keyword().lower() in ['let' , 'do' , 'if' ,'while' , 'return']:
                return False
        self.write_opening_tag("varDec")
        while self.input.symbol() != ";":
            self.write_wrap()
            self.input.advance()
        self.write_wrap()  #;#
        self.input.advance()
        self.write_closing_tag("varDec")
        return True

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        self.write_opening_tag("statements")
        while self.input.token_type() != "SYMBOL": # until "}"

            letter = self.input.keyword().lower()
            if letter == "let":
                self.compile_let()
            elif letter == "if":
                self.compile_if()
            elif letter == "while":
                self.compile_while()
            elif letter == "do":
                self.compile_do()
            elif letter == "return":
                self.compile_return()
        self.write_closing_tag("statements")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!

        self.write_opening_tag("doStatement")
        self.write_wrap() #do
        self.input.advance()
        self.write_wrap() 
        self.input.advance()
        self.compile_subroutine_call()
        self.write_wrap() #;
        self.input.advance()
        self.write_closing_tag("doStatement")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        self.write_opening_tag("letStatement")
        self.write_wrap() #let
        self.input.advance()
        self.write_wrap()   #var name
        self.input.advance()
        if self.input.token_type() == "SYMBOL":  #expression
            if self.input.symbol() == "[":
                self.write_wrap()  #[#
                self.input.advance()
                self.compile_expression()
                self.write_wrap()   #]#
                self.input.advance()
        self.write_wrap()    # = #
        self.input.advance()
        self.compile_expression()

        self.write_wrap()   # ";"
        self.input.advance()
        self.write_closing_tag("letStatement")

    def compile_while(self) -> None:   #todo -> to check function with while
        """Compiles a while statement."""
        # Your code goes here!
        self.write_opening_tag("whileStatement")

        self.write_wrap()   #while
        self.input.advance()
        self.write_wrap()  # (
        self.input.advance()
        self.compile_expression()
        self.write_wrap()   #)
        self.input.advance()
        self.write_wrap()   #{
        self.input.advance() 
        self.compile_statements()
        self.write_wrap() # }
        self.input.advance()
        self.write_closing_tag("whileStatement")


    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        self.write_opening_tag("returnStatement")

        self.write_wrap()
        self.input.advance()
        if self.input.symbol() == ";":
            self.write_wrap()
            self.input.advance()
        else:
            self.compile_expression()
            self.write_wrap()
            self.input.advance()
        self.write_closing_tag("returnStatement")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        self.write_opening_tag("ifStatement")
        self.write_wrap() #if
        self.input.advance()
        self.write_wrap()  # "(" ->open expression
        self.input.advance()
        self.compile_expression()
        self.write_wrap()  # ")"  -> close expression
        self.input.advance()
        self.write_wrap()    # { -->open statement
        self.input.advance()
        self.compile_statements()
        self.write_wrap()  #  " } " -->close statement
        self.input.advance()
        if self.input.token_type() == "KEYWORD":   #todo: to check function with else
            if self.input.keyword() == "ELSE" :
                self.write_wrap() #else
                self.input.advance()
                self.write_wrap() #{
                self.input.advance()
                self.compile_statements()
                self.write_wrap() #} 
                self.input.advance()
        self.write_closing_tag("ifStatement")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        self.write_opening_tag("expression")
        self.compile_term() #term or op   #todo: maybe i should check of its term or operator (op)
        if self.input.token_type() == "SYMBOL":
            if self.input.symbol() in self.unary_op:
                self.write_wrap()
                self.input.advance()
                self.compile_term()
        self.write_closing_tag("expression")

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
        # Your code goes here!
        self.write_opening_tag("term")
        if self.input.token_type() == "INT_CONST" or self.input.token_type() == "STRING_CONST":
            self.write_wrap()
            self.input.advance()
        elif self.input.token_type() == "KEYWORD":
            if self.input.keyword().lower() == 'true' or 'false' or 'null' or 'this':
                self.write_wrap()
                self.input.advance()
        elif self.input.token_type() == "SYMBOL":
            if self.input.symbol() == '(':
                self.write_wrap()
                self.input.advance()
                self.compile_expression()
                self.write_wrap()
                self.input.advance()
            elif self.input.symbol() == '-' or '~':
                self.write_wrap()
                self.input.advance()
                self.compile_term()
            
        elif self.input.token_type() == "IDENTIFIER":
            self.write_wrap()
            self.input.advance()
            if self.input.token_type() != "SYMBOL":
                pass
            else:
                if self.input.symbol() == '(' or self.input.symbol() == '.' :
                    self.compile_subroutine_call()
                    
                elif self.input.symbol() == '[':
                    self.write_wrap()
                    self.input.advance()
                    self.compile_expression()
                    self.write_wrap()
                    self.input.advance()
        self.write_closing_tag("term")
                    
    def compile_subroutine_call(self):
        if self.input.symbol() == '(' :
            self.write_wrap()
            self.input.advance()
            self.compile_expression_list()
            self.write_wrap()
            self.input.advance()
        elif self.input.symbol() == '.':
            self.write_wrap()
            self.input.advance()
            self.write_wrap()
            self.input.advance()
            self.write_wrap()
            self.input.advance()
            self.compile_expression_list()
            self.write_wrap()
            self.input.advance()

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        self.write_opening_tag("expressionList")
        if self.input.symbol() != ")":

            self.compile_expression()
            while self.input.symbol() == ",":
                self.write_wrap()
                self.input.advance()
                self.compile_expression()
        else:
            pass
        self.write_closing_tag("expressionList")

    def write(self, string1):
        self.output_stream.write(string1)

    def write_wrap(self):
        type1 = self.input.token_type()
        if type1 == "KEYWORD":
            word = self.input.keyword().lower()
            type1 = type1.lower()
        elif type1 == "SYMBOL":
            word = self.input.symbol()

            type1 = type1.lower()
        elif type1 == "INT_CONST":
            word = self.input.int_val()
            type1 = "integerConstant"
        elif type1 == "STRING_CONST":
            word = self.input.string_val()
            word = word[1:len(word) - 1]
            type1 = "stringConstant"
        elif type1 == "IDENTIFIER":
            word = self.input.identifier()
            type1 = type1.lower()
        self.write("<" + type1 + "> " + word + " </" + type1 + ">\n" )

        #todo -> this just for debuag
        if(self.check==1) :
             print("<" + type1 + "> " + word + " </" + type1 + ">\n" )
             self.check=0


