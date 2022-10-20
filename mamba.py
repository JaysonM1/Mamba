#########################
#           DIGITS      #
#########################


from fnmatch import fnmatchcase


DIGITS = "0123456789"

######################
#        ERRORS      #
######################


class Error:
    def __init__(self, position_start, position_end, error_name, details) -> None:
        self.pos_start = position_start
        self.pos_end = position_end
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.filename}, line {self.pos_start.line + 1}'
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details) -> None:
        super().__init__(pos_start, pos_end, "Illegal Character", details)

################################
#            POSITION          #
################################

class Position:
    def __init__(self, idx, ln, col,fn, ftxt) -> None:
        self.index = idx
        self.line = ln
        self.column = col
        self.filename = fn
        self.filetxt = ftxt

    def advance(self, curr_char):
        self.index += 1
        self.column += 1
        
        if curr_char == '\n':
            self.line += 1
            self.column = 0
        return self

    def copy(self):
        return Position(self.index, self.line, self.column, self.filename, self.filetxt)
################################
#          TOKENS              #
################################


TOKEN_INT = 'INT'
TOKEN_FLOAT = 'FLOAT'
TOKEN_PLUS = 'PLUS'
TOKEN_MINUS = 'MINUS'
TOKEN_MULITPLY = 'MULTIPLY'
TOKEN_DIVIDE = 'DIVIDE'
TOKEN_LPAREN = 'LPAREN'
TOKEN_RPAREN = 'RPAREN'

class Token:
    def __init__(self, type, value = None) -> None:
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        if self.value:
            return f'{self.type} = {self.value}'
        return f'{self.type}'


#########################
#        LEXER          #
#########################

class Lexer:
    def __init__(self, fn, text) -> None:
        self.filename = fn
        self.text = text
        self.position = Position(-1,0,-1, fn, text)
        self.curr_char = None
        self.advance()

    def advance(self) -> None:
        self.position.advance(self.curr_char)
        if self.position.index < len(self.text):
            self.curr_char = self.text[self.position.index]
        else:
            self.curr_char = None
        
    def make_tokens(self):
        tokens = []

        while self.curr_char != None:
            if self.curr_char == ' ':
                self.advance()
            elif self.curr_char in DIGITS:
                tokens.append(self.make_numbers())
            elif self.curr_char == '+':
                tokens.append(Token(TOKEN_PLUS))
                self.advance()
            elif self.curr_char == '-':
                tokens.append(Token(TOKEN_MINUS))
                self.advance()
            elif self.curr_char == '*':
                tokens.append(Token(TOKEN_MULITPLY))
                self.advance()
            elif self.curr_char == '/':
                tokens.append(Token(TOKEN_DIVIDE))
                self.advance()
            elif self.curr_char == ')':
                tokens.append(Token(TOKEN_RPAREN))
                self.advance()
            elif self.curr_char == '(':
                tokens.append(Token(TOKEN_LPAREN))
                self.advance()
            else:
                pos_start = self.position.copy()
                char = self.curr_char
                self.advance()
                return [], IllegalCharError(pos_start, self.position, "'" + char + "'")


        return tokens, None


    def make_numbers(self) -> Token:
        num_str = ''
        dot_count = 0

        while self.curr_char != None and self.curr_char in DIGITS + '.':
            if self.curr_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.curr_char
            self.advance()

        if dot_count == 0:
            return Token(TOKEN_INT, int(num_str))
        else:
            return Token(TOKEN_FLOAT, float(num_str))









def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    return tokens, error