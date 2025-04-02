


class Bla:
    def __init__(self) -> None:
        self.keyword = ['class' , 'constructor' , 'function' , 'method' , 'field' , 
               'static' , 'var' , 'int' , 'char' , 'boolean' , 'void' , 'true' ,
               'false' , 'null' , 'this' , 'let' , 'do' , 'if' , 'else' , 
               'while' , 'return' ]
        self.symbols = ['{' , '}' , '(' , ')' , '[' , ']' , '.' , ',' , ';' , '+' , 
              '-' , '*' , '/' , '&' , '|' , '<' , '>' , '=' , '~' , '^' , '#']
        self.input_lines = """// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/10/Square/Square.jack

// (same as projects/09/Square/Square.jack)

/** Implements a graphical square. */
class Square {

   field int x, y; // screen location of the square's top-left corner
   field int size; // length of this square, in pixels

   /** Constructs a new square with a given location and size. */
   constructor Square new(int Ax, int Ay, int Asize) {
      let x = Ax;
      let y = Ay;
      let size = Asize;
      do draw();
      return this;
   }

   /** Disposes this square. */
   method void dispose() {
      do Memory.deAlloc(this);
      return;
   }

   /** Draws the square on the screen. */
   method void draw() {
      do Screen.setColor(true);
      do Screen.drawRectangle(x, y, x + size, y + size);
      return;
   }

   /** Erases the square from the screen. */
   method void erase() {
      do Screen.setColor(false);
      do Screen.drawRectangle(x, y, x + size, y + size);
      return;
   }

    /** Increments the square size by 2 pixels. */
   method void incSize() {
      if (((y + size) < 254) & ((x + size) < 510)) {
         do erase();
         let size = size + 2;
         do draw();
      }
      return;
   }

   /** Decrements the square size by 2 pixels. */
   method void decSize() {
      if (size > 2) {
         do erase();
         let size = size - 2;
         do draw();
      }
      return;
   }

   /** Moves the square up by 2 pixels. */
   method void moveUp() {
      if (y > 1) {
         do Screen.setColor(false);
         do Screen.drawRectangle(x, (y + size) - 1, x + size, y + size);
         let y = y - 2;
         do Screen.setColor(true);
         do Screen.drawRectangle(x, y, x + size, y + 1);
      }
      return;
   }

   /** Moves the square down by 2 pixels. */
   method void moveDown() {
      if ((y + size) < 254) {
         do Screen.setColor(false);
         do Screen.drawRectangle(x, y, x + size, y + 1);
         let y = y + 2;
         do Screen.setColor(true);
         do Screen.drawRectangle(x, (y + size) - 1, x + size, y + size);
      }
      return;
   }

   /** Moves the square left by 2 pixels. */
   method void moveLeft() {
      if (x > 1) {
         do Screen.setColor(false);
         do Screen.drawRectangle((x + size) - 1, y, x + size, y + size);
         let x = x - 2;
         do Screen.setColor(true);
         do Screen.drawRectangle(x, y, x + 1, y + size);
      }
      return;
   }

   /** Moves the square right by 2 pixels. */
   method void moveRight() {
      if ((x + size) < 510) {
         do Screen.setColor(false);
         do Screen.drawRectangle(x, y, x + 1, y + size);
         let x = x + 2;
         do Screen.setColor(true);
         do Screen.drawRectangle((x + size) - 1, y, x + size, y + size);
      }
      return;
   }
}"""
        self.pre_tokens1 = self.delete_comments()
        self.pre_tokens1 = self.pre_tokens1.splitlines()
        self.pre_tokens = []
        self.tokens = []
        self.seperate_strings(self.pre_tokens1)
        self.seperate_tokens()
        self.tokens_counter = 0
        self.num_of_tokens = len(self.tokens)
        self.cur_token = self.tokens[0]
    def print(self):
        for i in self.tokens:
            print(i)
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
                self.tokens.append(line[1:len(line) - 1])
            else:
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
if "__main__" == __name__:
    tokenizer = Bla()
    tokenizer.print()




