from enum import Enum


class TokenType(Enum):
    T_SEMICOLON = 0  # ';'
    T_OPEN_PAREN = 1  # '('
    T_CLOSE_PAREN = 2  # ')'
    T_OPEN_BRAKE = 3  # '['
    T_CLOSE_BRAKE = 4  # ']'
    T_OPEN_BRACE = 5  # '{'
    T_CLOSE_BRACE = 6  # '}'
    T_COMMENT = 7  # '#'
    T_STRING = 8  # "string"
    T_INT = 9  # int
    T_DOUBLE = 10  # double
    T_BOOL = 11  # bool
    T_TRUE = 12  # true
    T_FALSE = 13  # false
    T_IF = 14  # if
    T_ELIF = 15  # elif
    T_ELSE = 16  # else
    T_WHILE = 17  # while
    T_METHOD = 18  # method

    T_ID = 20  # variables
    T_ASSIGN = 21  # =
    T_EQUAL_OP = 22  # ==
    T_NOT = 23  # !
    T_DIFF_OP = 24  # !=
    T_ADD_OP = 25  # +
    T_ADD_AS = 26  # +=
    T_SUB_OP = 27  # -
    T_SUB_AS = 28  # -=
    T_MUL_OP = 29  # *
    T_MUL_AS = 30  # *=
    T_EXP_OP = 31  # **
    T_EXP_AS = 32  # **=
    T_DIV_OP = 33  # /
    T_DIV_AS = 34  # /=
    T_MOD_OP = 35  # %
    T_MOD_AS = 36  # %=
    T_LESS_OP = 37  # <
    T_LEQ_OP = 38  # <=
    T_GREAT_OP = 39  # >
    T_GRQ_OP = 40  # >=
    T_AND_OP = 41  # &&
    T_AND_AS = 42  # &=
    T_OR_OP = 43  # ||
    T_OR_AS = 44  # ||=
    T_XOR_OP = 45  # ^
    T_XOR_AS = 46  # ^=

    T_DOT = 50  # .
    T_COMMA = 51  # ,
    T_COLON = 52  # :

    T_CARRIAGE = 60  # \r
    T_NEWLINE = 61  # \n

    T_INVALID = 90


class Token:
    def __init__(self, line: int, column: int, token_type: TokenType, lexeme=None):
        self.line = line
        self.column = column
        self.token_type = token_type
        self.lexeme = lexeme

    def print_token(self):
        print("LINE:", self.line)
        print("COLUMN:", self.column)
        print("TYPE:", self.token_type)
        if self.lexeme is not None:
            print("LEXEME:", self.lexeme)


def predefine() -> (dict, dict, dict):
    keywords = dict([("bool", TokenType.T_BOOL), ("break", TokenType.T_BOOL), ("continue", TokenType.T_BOOL),
                     ("double", TokenType.T_DOUBLE), ("elif", TokenType.T_ELIF), ("else", TokenType.T_ELSE),
                     ("false", TokenType.T_FALSE), ("if", TokenType.T_IF), ("include", TokenType.T_FALSE),
                     ("int", TokenType.T_INT), ("method", TokenType.T_METHOD), ("null", TokenType.T_BOOL),
                     ("return", TokenType.T_STRING), ("string", TokenType.T_STRING), ("true", TokenType.T_TRUE),
                     ("void", TokenType.T_WHILE), ("while", TokenType.T_WHILE)])
    operators = dict([("=", TokenType.T_ASSIGN), ("==", TokenType.T_EQUAL_OP),
                      ("!", TokenType.T_NOT), ("!=", TokenType.T_DIFF_OP),
                      ("+", TokenType.T_ADD_OP), ("+=", TokenType.T_ADD_AS),
                      ("-", TokenType.T_SUB_OP), ("-=", TokenType.T_SUB_AS),
                      ("*", TokenType.T_MUL_OP), ("*=", TokenType.T_MUL_AS),
                      ("**", TokenType.T_EXP_OP), ("**=", TokenType.T_EXP_AS),
                      ("/", TokenType.T_DIV_OP), ("/=", TokenType.T_DIV_AS),
                      ("%", TokenType.T_MOD_OP), ("%=", TokenType.T_MOD_AS),
                      ("<", TokenType.T_LESS_OP), ("<=", TokenType.T_LEQ_OP),
                      (">", TokenType.T_GREAT_OP), (">=", TokenType.T_GRQ_OP),
                      ("&&", TokenType.T_AND_OP), ("&&=", TokenType.T_AND_AS),
                      ("||", TokenType.T_OR_OP), ("||=", TokenType.T_OR_AS),
                      ("^", TokenType.T_XOR_OP), ("^=", TokenType.T_XOR_AS)])
    punctuators = dict([('.', TokenType.T_DOT), (',', TokenType.T_COMMA), (':', TokenType.T_COLON)])
    return keywords, operators, punctuators
