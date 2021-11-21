from enum import Enum


class TokenType(Enum):
    T_SEMICOLON = 0  # ';'
    T_OPEN_PAREN = 1  # '('
    T_CLOSE_PAREN = 2  # ')'
    T_OPEN_BRACKET = 3  # '['
    T_CLOSE_BRACKET = 4  # ']'
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
    def __init__(self, token_type: TokenType, line: int, column: int, value=None):
        self.token_type = token_type
        self.line = line
        self.column = column
        self.value = value

    def __repr__(self):
        return self.string() + ", line {}, column {}".format(self.line, self.column)

    def string(self):
        string = "{}".format(self.token_type.name)
        if self.value is not None:
            string += ": {}".format(self.value)
        return string
