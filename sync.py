import re
TOKEN_IDENTIFIER = "変数"
TOKEN_NUMBER = "NUMBER"
TOKEN_IF = "もし"
TOKEN_ADDITION = 'TOKEN_ADDITION'
TOKEN_ASSIGN = 'TOKEN_ASSIGN'
TOKEN_MINUS = "TOKEN_MINUS"
TOKEN_DIVIDE = "TOKEN_DIVIDE"
TOKEN_MULTIPLY = "TOKEN_MULTIPLY"
TOKEN_OPERATOR = "OPERATOR"
TOKEN_GREATERTHAN = "TOKEN_GREATERTHAN"
TOKEN_LESSTHAN = "TOKEN_LESSTHAN"
TOKEN_BRACKET1FUNCTION = "TOKEN_BRACKET1FUNCTION"
TOKEN_BRACKET2FUNCTION = "TOKEN_BRACKET2FUNCTION"
TOKEN_PARAMETER1FUNCTION = "TOKEN_PARAMETER1FUNCTION"
TOKEN_PARAMETER2FUNCTION = "TOKEN_PARAMETER2FUNCTION"
TOKEN_LOOP = "ループ"
TOKEN_PRINT = "表示"
TOKEN_BREAK = "打破"
LESS_THAN_EQUAL_TO = "<="
GREATER_THAN_EQUAL_TO = ">="
TOKEN_CONNECT_LIBRARY = "繋ぐ"
TOKEN_FUNCTION = "関数"
hiraganaphrases = {
    "あ","え","う","お","わ","い","さ","せ","そ","ま","し","て","た","ゆ","や"
    ,"れ","ろ","こ","よ","ぞ","ん","ち","ひ","と","ら","る","か","け","く","き",
    "り","み","ざ","ば","は","じ","ぽ","い","び","べ","へ","ぴ","ぺ","ふ","ぶ","な","に","が","ご"
}

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
        self.digits = 0
class Tokenizer:
    def __init__(self, input_str):
        self.input = input_str
        self.pos = 0
    def get_next_token(self):
        while self.pos < len(self.input) and self.input[self.pos].isspace():
            self.pos += 1
        if self.pos >= len(self.input):
            return None

        if self.input[self.pos] == '=':
            self.pos += 1
            return Token(TOKEN_ASSIGN, '=')

        if self.input[self.pos:self.pos+2] == '表示':
            self.pos += 2
            return Token(TOKEN_PRINT, '表示')
        
        if self.input[self.pos:self.pos+2] == '打破':
            self.pos += 2
            return Token(TOKEN_BREAK, '打破')
        
        if self.input[self.pos:self.pos+2] == '関数':
            self.pos += 2
            return Token(TOKEN_FUNCTION, '関数')

        if self.input[self.pos:self.pos+2] == '<=':
            self.pos += 2
            return Token(LESS_THAN_EQUAL_TO, '<=')

        if self.input[self.pos:self.pos+2] == '>=':
            self.pos += 2
            return Token(GREATER_THAN_EQUAL_TO, '>=')

        if self.input[self.pos] == '-':
            self.pos += 1
            return Token(TOKEN_MINUS, '-')

        if self.input[self.pos:self.pos+2] == 'もし':
            self.pos += 2
            return Token(TOKEN_IF, 'もし')
        
        if self.input[self.pos:self.pos+3] == 'ループ':
            self.pos += 3
            return Token(TOKEN_IF, 'ループ')

        if self.input[self.pos] == '/':
            self.pos += 1
            return Token(TOKEN_DIVIDE, '/')
        
        if self.input[self.pos] == '*':
            self.pos += 1
            return Token(TOKEN_MULTIPLY, '*')
        
        if self.input[self.pos] == '+':
            self.pos += 1
            return Token(TOKEN_ADDITION, '+')
        
        if self.input[self.pos] == '>':
            self.pos += 1
            return Token(TOKEN_GREATERTHAN, '>')

        if self.input[self.pos] == '<':
            self.pos += 1
            return Token(TOKEN_LESSTHAN, '<')
        
        if self.input[self.pos] == '{':
            self.pos += 1
            return Token(TOKEN_BRACKET1FUNCTION, '{')

        if self.input[self.pos] == '}':
            self.pos += 1
            return Token(TOKEN_BRACKET2FUNCTION, '}')
        
        if self.input[self.pos] == '(':
            self.pos += 1
            return Token(TOKEN_PARAMETER1FUNCTION, '(')

        if self.input[self.pos] == ')':
            self.pos += 1
            return Token(TOKEN_PARAMETER2FUNCTION, ')')
        match_identifier = re.match(r'[' +''.join(hiraganaphrases) + r']+', self.input[self.pos:])
        if match_identifier:
            value = match_identifier.group(0)
            self.pos += len(value)
            return Token(TOKEN_IDENTIFIER, value)
        match_number = re.match(r'\d+', self.input[self.pos:])
        if match_number:
            value = match_number.group(0)
            self.pos += len(value)
            return Token(TOKEN_NUMBER, int(value))
        return None