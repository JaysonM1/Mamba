########
#DIGITS#
########


DIGITS = "0123456789"

########
#ERRORS#
########


class Error:
    def __init__(self, error_name, details) -> None:
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        return f'{self.error_name}: {self.details}'


class IllegalCharError(Error):
    def __init__(self, details) -> None:
        super().__init__("Illegal Character", details)
########
#TOKENS#
########


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


#######
#LEXER#
#######

class Lexer:
    def __init__(self,text) -> None:
        self.text = text
        self.position = -1
        self.curr_char = None
        self.advance()

    def advance(self) -> None:
        self.position += 1
        if self.position < len(self.text):
            self.curr_char = self.text[self.position]
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
                char = self.curr_char
                self.advance()
                return [], IllegalCharError("'" + char + "'")


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









def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    return tokens, error