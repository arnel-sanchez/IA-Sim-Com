from compilation.tokens import TokenType, Token
from compilation.errors import Error, UnknownCharacterError, UnexpectedCharacterError, UnbalancedBracketsError


class Tokenizer:
    def __init__(self):
        self.keywords = dict([("bike", TokenType.T_BIKE), ("bool", TokenType.T_BOOL), ("break", TokenType.T_BREAK),
                              ("continue", TokenType.T_CONTINUE), ("double", TokenType.T_DOUBLE),
                              ("elif", TokenType.T_ELIF), ("else", TokenType.T_ELSE), ("false", TokenType.T_FALSE),
                              ("if", TokenType.T_IF), ("include", TokenType.T_INCLUDE), ("int", TokenType.T_INT),
                              ("method", TokenType.T_METHOD), ("null", TokenType.T_NULL),
                              ("return", TokenType.T_RETURN), ("rider", TokenType.T_RIDER),
                              ("string", TokenType.T_STRING), ("true", TokenType.T_TRUE), ("void", TokenType.T_VOID),
                              ("while", TokenType.T_WHILE)])
        self.operators = dict([("=", TokenType.T_ASSIGN), ("==", TokenType.T_EQ_REL),
                               ("!", TokenType.T_NEG_OP), ("!=", TokenType.T_NEQ_REL),
                               ("+", TokenType.T_ADD_OP), ("+=", TokenType.T_ADD_AS),
                               ("-", TokenType.T_SUB_OP), ("-=", TokenType.T_SUB_AS),
                               ("*", TokenType.T_MUL_OP), ("*=", TokenType.T_MUL_AS),
                               ("**", TokenType.T_EXP_OP), ("**=", TokenType.T_EXP_AS),
                               ("/", TokenType.T_DIV_OP), ("/=", TokenType.T_DIV_AS),
                               ("%", TokenType.T_MOD_OP), ("%=", TokenType.T_MOD_AS),
                               ("<", TokenType.T_LESS_REL), ("<=", TokenType.T_LEQ_REL),
                               (">", TokenType.T_GREAT_REL), (">=", TokenType.T_GREQ_REL),
                               ("&&", TokenType.T_AND_OP), ("&&=", TokenType.T_AND_AS),
                               ("||", TokenType.T_OR_OP), ("||=", TokenType.T_OR_AS),
                               ("^", TokenType.T_XOR_OP), ("^=", TokenType.T_XOR_AS)])
        self.punctuators = dict([('.', TokenType.T_DOT), (',', TokenType.T_COMMA), (':', TokenType.T_COLON)])
        self.input_text = ""
        self.f_pointer = 0
        self.s_pointer = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.error = None

    def tokenize(self, file: str, input_text: str) -> ([Token], Error):
        self.input_text = input_text
        self.f_pointer = 0
        self.s_pointer = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.error = None
        open_parens = 0
        open_brackets = 0
        open_braces = 0
        while self.f_pointer < len(self.input_text) and self.error is None:
            current = self.input_text[self.f_pointer]
            if current == ' ' or current == '\t':
                pass
            elif current == '\n':
                self.line += 1
                self.column = 0
            elif current == '\r':
                if self.f_pointer + 1 < len(self.input_text) and self.input_text[self.f_pointer + 1] == '\n':
                    self.f_pointer += 1
                self.line += 1
                self.column = 0
            elif current == ';':
                self.tokens.append(Token(TokenType.T_SEMICOLON, self.line, self.column))
            elif current == '(':
                open_parens += 1
                self.tokens.append(Token(TokenType.T_OPEN_PAREN, self.line, self.column))
            elif current == ')':
                open_parens -= 1
                self.tokens.append(Token(TokenType.T_CLOSE_PAREN, self.line, self.column))
            elif current == '[':
                open_brackets += 1
                self.tokens.append(Token(TokenType.T_OPEN_BRACKET, self.line, self.column))
            elif current == ']':
                open_brackets -= 1
                self.tokens.append(Token(TokenType.T_CLOSE_BRACKET, self.line, self.column))
            elif current == '{':
                open_braces += 1
                self.tokens.append(Token(TokenType.T_OPEN_BRACE, self.line, self.column))
            elif current == '}':
                open_braces -= 1
                self.tokens.append(Token(TokenType.T_CLOSE_BRACE, self.line, self.column))
            elif current == '#' or current == '\"':
                self.comment_string(current)
            elif current.isnumeric():
                self.number(file)
            elif current.isalpha() or current == "_":
                self.alpha()
            else:
                op = self.operators.get(current)
                if op or current in ["&", "|"]:
                    self.operator(current, op)
                else:
                    pct = self.punctuators.get(current)
                    if pct:
                        self.tokens.append(Token(pct, self.line, self.column))
                    else:
                        self.tokens = []
                        self.error = UnknownCharacterError(current, file, self.line, self.column)
                        break
            self.f_pointer += 1
            self.column += self.f_pointer - self.s_pointer
            self.s_pointer = self.f_pointer
        if self.error is None:
            self.balanced(file, open_parens, open_brackets, open_braces)
        return self.tokens, self.error

    def comment_string(self, char: str):
        token = ""
        while self.f_pointer < len(self.input_text):
            self.f_pointer += 1
            if self.input_text[self.f_pointer] == char:
                break
            token += self.input_text[self.f_pointer]
        self.tokens.append(Token(TokenType.T_COMMENT if char == '#' else TokenType.T_S_VALUE, self.line, self.column,
                                 token))

    def number(self, file: str):
        token = ""
        double = False
        error = False
        while self.f_pointer < len(self.input_text) and (self.input_text[self.f_pointer].isnumeric() or
                                                         self.input_text[self.f_pointer] == '.'):
            token += self.input_text[self.f_pointer]
            if self.input_text[self.f_pointer] == '.':
                if double:
                    error = True
                    break
                double = True
            self.f_pointer += 1
        if error or (self.f_pointer < len(self.input_text) and self.input_text[self.f_pointer].isalpha()):
            self.error = UnexpectedCharacterError(self.input_text[self.f_pointer], file, self.line,
                                                  self.column + self.f_pointer - self.s_pointer)
            return
        if double:
            self.tokens.append(Token(TokenType.T_D_VALUE, self.line, self.column, float(token)))
        else:
            self.tokens.append(Token(TokenType.T_I_VALUE, self.line, self.column, int(token)))
        self.f_pointer -= 1

    def alpha(self):
        token = ""
        while self.f_pointer < len(self.input_text) and (self.input_text[self.f_pointer].isalpha()
                                                         or self.input_text[self.f_pointer].isnumeric()
                                                         or self.input_text[self.f_pointer] == "_"):
            token += self.input_text[self.f_pointer]
            self.f_pointer += 1
        keyword = self.keywords.get(token)
        if keyword:
            self.tokens.append(Token(keyword, self.line, self.column))
        else:
            self.tokens.append(Token(TokenType.T_ID, self.line, self.column, token))
        self.f_pointer -= 1

    def operator(self, token: str, op: TokenType):
        while self.f_pointer + 1 < len(self.input_text):
            self.f_pointer += 1
            token += self.input_text[self.f_pointer]
            new_opt = self.operators.get(token)
            if not new_opt:
                break
            op = new_opt
        self.tokens.append(Token(op, self.line, self.column))
        self.f_pointer -= 1

    def balanced(self, file: str, open_parens: int, open_brackets: int, open_braces: int):
        if open_parens > 0:
            self.error = UnbalancedBracketsError("(", file, self.line, self.column)
        elif open_parens < 0:
            self.error = UnbalancedBracketsError(")", file, self.line, self.column)
        elif open_brackets > 0:
            self.error = UnbalancedBracketsError("[", file, self.line, self.column)
        elif open_brackets < 0:
            self.error = UnbalancedBracketsError("]", file, self.line, self.column)
        elif open_braces > 0:
            self.error = UnbalancedBracketsError("{", file, self.line, self.column)
        elif open_braces < 0:
            self.error = UnbalancedBracketsError("}", file, self.line, self.column)
