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
    T_NULL = 12  # null

    T_TRUE = 13  # true
    T_FALSE = 14  # false

    T_IF = 15  # if
    T_ELIF = 16  # elif
    T_ELSE = 17  # else

    T_WHILE = 18  # while
    T_CONTINUE = 19  # continue
    T_BREAK = 20  # break

    T_METHOD = 21  # method
    T_VOID = 22  # void
    T_RETURN = 23  # return

    T_INCLUDE = 24  # include

    T_ID = 25  # variables

    T_S_VALUE = 26  # some string value
    T_I_VALUE = 27  # some int value
    T_D_VALUE = 28  # some double value

    T_ADD_OP = 29  # +
    T_SUB_OP = 30  # -
    T_NEG_OP = 31  # !
    T_MUL_OP = 32  # *
    T_DIV_OP = 33  # /
    T_MOD_OP = 34  # %
    T_EXP_OP = 35  # **

    T_EQ_REL = 36  # ==
    T_NEQ_REL = 37  # !=

    T_LESS_REL = 38  # <
    T_LEQ_REL = 39  # <=
    T_GREAT_REL = 41  # >
    T_GREQ_REL = 41  # >=

    T_AND_OP = 42  # &&
    T_OR_OP = 43  # ||
    T_XOR_OP = 44  # ^

    T_ASSIGN = 45  # =
    T_ADD_AS = 46  # +=
    T_SUB_AS = 47  # -=
    T_MUL_AS = 48  # *=
    T_DIV_AS = 49  # /=
    T_MOD_AS = 50  # %=
    T_EXP_AS = 51  # **=

    T_AND_AS = 52  # &&=
    T_OR_AS = 53  # ||=
    T_XOR_AS = 54  # ^=

    T_DOT = 55  # .
    T_COMMA = 56  # ,
    T_COLON = 57  # :

    T_CARRIAGE = 58  # \r
    T_NEWLINE = 59  # \n

    T_INVALID = 60  # invalid token


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
