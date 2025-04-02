"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    
    # Jack Language Grammar

    A Jack file is a stream of characters. If the file represents a
    valid program, it can be tokenized into a stream of valid tokens. The
    tokens may be separated by an arbitrary number of whitespace characters, 
    and comments, which are ignored. There are three possible comment formats: 
    /* comment until closing */ , /** API comment until closing */ , and 
    // comment until the line’s end.

    - ‘xxx’: quotes are used for tokens that appear verbatim (‘terminals’).
    - xxx: regular typeface is used for names of language constructs 
           (‘non-terminals’).
    - (): parentheses are used for grouping of language constructs.
    - x | y: indicates that either x or y can appear.
    - x?: indicates that x appears 0 or 1 times.
    - x*: indicates that x appears 0 or more times.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate 
    file. A compilation unit is a single class. A class is a sequence of tokens 
    structured according to the following context free syntax:
    
    - class: 'class' className '{' classVarDec* subroutineDec* '}'
    - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
    - type: 'int' | 'char' | 'boolean' | className
    - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) 
    - subroutineName '(' parameterList ')' subroutineBody
    - parameterList: ((type varName) (',' type varName)*)?
    - subroutineBody: '{' varDec* statements '}'
    - varDec: 'var' type varName (',' varName)* ';'
    - className: identifier
    - subroutineName: identifier
    - varName: identifier

    ## Statements

    - statements: statement* 
    - statement: letStatement | ifStatement | whileStatement | doStatement | 
                 returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
                   statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions
    
    - expression: term (op term)*
    - term: integerConstant | stringConstant | keywordConstant | varName | 
            varName '['expression']' | subroutineCall | '(' expression ')' | 
            unaryOp term
    - subroutineCall: subroutineName '(' expressionList ')' | (className | 
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - unaryOp: '-' | '~' | '^' | '#'
    - keywordConstant: 'true' | 'false' | 'null' | 'this'
    
    Note that ^, # correspond to shiftleft and shiftright, respectively.
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        self.keywords = ['class' , 'constructor' , 'function' , 'method' , 'field' , 
               'static' , 'var' , 'int' , 'char' , 'boolean' , 'void' , 'true' ,
               'false' , 'null' , 'this' , 'let' , 'do' , 'if' , 'else' , 
               'while' , 'return' ]
        self.symbols = ['{' , '}' , '(' , ')' , '[' , ']' , '.' , ',' , ';' , '+' , 
              '-' , '*' , '/' , '&' , '|' , '<' , '>' , '=' , '~' , '^' , '#']
        self.input_lines = input_stream.read()
        self.pre_tokens1 = self.delete_comments()
        self.pre_tokens1 = self.pre_tokens1.splitlines()
        self.pre_tokens = []
        self.tokens = []
        self.seperate_strings(self.pre_tokens1)
        self.seperate_tokens()
        self.tokens_counter = 0
        self.num_of_tokens = len(self.tokens) - 1
        self.cur_token = self.tokens[0]
        
        

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        # Your code goes here!
        if self.tokens_counter >= self.num_of_tokens:
            return False
        else:
            return True

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        # Your code goes here!
        self.tokens_counter += 1
        if self.has_more_tokens():
            self.cur_token = self.tokens[self.tokens_counter]

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        if self.cur_token in self.keywords:
            return "KEYWORD"
        elif self.cur_token in self.symbols:
            return "SYMBOL"
        elif self.cur_token[0].isdigit():
            return "INT_CONST"
        elif self.cur_token[0] == '"':
            return "STRING_CONST"
        else:
            return "IDENTIFIER"

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        # Your code goes here!
        return self.cur_token.upper()

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
            Recall that symbol was defined in the grammar like so:
            symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
        """
        # Your code goes here!
        if self.cur_token == "<":
            return "&lt;"
        elif self.cur_token == ">":
            return "&gt;"
        elif self.cur_token == '"':
            return "&quot;"
        elif self.cur_token == "&":
            return "&amp;" 
        return self.cur_token

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
            Recall that identifiers were defined in the grammar like so:
            identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.
        """
        # Your code goes here!
        return self.cur_token

    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
            Recall that integerConstant was defined in the grammar like so:
            integerConstant: A decimal number in the range 0-32767.
        """
        # Your code goes here!
        if int(self.cur_token) >=0 and int(self.cur_token) < 32768 :
            return self.cur_token

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double 
            quotes. Should be called only when token_type() is "STRING_CONST".
            Recall that StringConstant was defined in the grammar like so:
            StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
        """
        # Your code goes here!
        return self.cur_token

    def delete_comments(self):
        ## deletes all comments
        lines_input = self.input_lines
        lines_input1 = ""
        lines_input2 = ""
        text = ""
        if "/*" or "/**" or "//" in lines_input:
            while "/*" in lines_input :
                ## find a start comment   
                index_start_1 = lines_input.find("/*")

                index_end_1 = lines_input.find("*/")    ## find the end of comment
                lines_input1 += lines_input[:index_start_1]    ## add to the new text the text before the comment
                lines_input = lines_input[index_end_1 + 2:]     ## check the next time only after the comment ends
            lines_input1 += lines_input
            while "/**" in lines_input1 :
                ## find a start comment   
                index_start_1 = lines_input1.find("/**")

                index_end_1 = lines_input1.find("*/")    ## find the end of comment
                lines_input2 += lines_input1[:index_start_1]    ## add to the new text the text before the comment
                lines_input1 = lines_input1[index_end_1 + 2:] 
            lines_input2 += lines_input1
            while "//" in lines_input2:  ## find a comment
                index_start_1 = lines_input2.find("//") 
                text += lines_input2[:index_start_1]
                lines_input2 = lines_input2[index_start_1 + 2:]
                end_of_line = lines_input2.find("\n")
                lines_input2 = lines_input2[end_of_line:] if end_of_line != -1 else ""
            text += lines_input2
        else:
            return lines_input
        return text
    def seperate_strings(self, lines_):
        for line in lines_:
            if '"' in line:
                start_index = line.find('"')
                rest = line[start_index + 1:]
                end_index = rest.find('"') + start_index + 1
                if start_index == 0 and end_index == len(line) - 1:
                    self.pre_tokens.append(line)
                elif start_index == 0 and end_index != len(line) - 1:
                    self.pre_tokens.append(line[:end_index + 1])
                    self.seperate_strings([line[end_index+1:]])
                elif start_index != 0 and end_index == len(line) - 1:
                    self.pre_tokens.append(line[:start_index])
                    self.pre_tokens.append(line[start_index:len(line)])
                else:
                    self.pre_tokens.append(line[:start_index])
                    self.pre_tokens.append(line[start_index:end_index + 1])
                    self.seperate_strings([line[end_index+1:]])
            else:
                self.pre_tokens.append(line)

    def seperate_tokens(self):
        for line in self.pre_tokens:
            tryit = line.split()
            if tryit == []:
                continue
            if line[0] == '"':
                self.tokens.append(line[0:len(line)])
                continue
            words = line.split()
            for section in words:
                self.append_until_symbol(section)

    def append_until_symbol(self, section):
        counter = 0
        word = ""
        for letter in section:
            if letter in self.symbols:
                if word != "":
                    self.tokens.append(word)
                    self.tokens.append(letter)
                    word = ""
                else:
                    self.tokens.append(letter)
                
                # if section[counter + 1:] != "":
                #     self.append_until_symbol(section[counter + 1:])
            else:
                word += letter
                counter += 1
        if word != "":
            self.tokens.append(word)