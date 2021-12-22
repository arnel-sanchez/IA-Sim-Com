from compilation.tokens import Token, TokenType
from compilation.errors import Error


class Node:
    def eval(self, variables: dict):
        return None

    def __repr__(self) -> str:
        return "NODE()"


class Simple(Node):
    def __init__(self, token: Token):
        self.token = token

    def eval(self, variables: dict):
        return self.token.value

    def __repr__(self) -> str:
        return "{}({})".format(self.type(), self.eval({}))

    @staticmethod
    def type() -> str:
        return "SIMPLE"


class String(Simple):
    def __init__(self, token: Token):
        super().__init__(token)
        if token.token_type != TokenType.T_S_VALUE:
            raise Exception#

    @staticmethod
    def type() -> str:
        return "STRING"


class Number(Simple):
    def __init__(self, token: Token):
        super().__init__(token)


class Int(Number):
    def __init__(self, token: Token):
        super().__init__(token)
        if token.token_type != TokenType.T_I_VALUE:
            raise Exception#

    @staticmethod
    def type() -> str:
        return "INT"


class Double(Number):
    def __init__(self, token: Token):
        super().__init__(token)
        if token.token_type != TokenType.T_D_VALUE:
            raise Exception#

    @staticmethod
    def type() -> str:
        return "DOUBLE"


class Bool(Simple):
    def __init__(self, token: Token):
        super().__init__(token)
        if token.token_type != (TokenType.T_TRUE and TokenType.T_FALSE):
            raise Exception#

    def eval(self, variables: dict) -> bool:
        return True if self.token.token_type == TokenType.T_TRUE else False

    @staticmethod
    def type() -> str:
        return "BOOL"


class Null(Simple):
    def __init__(self, token: Token):
        super().__init__(token)
        if token.token_type != TokenType.T_NULL:
            raise Exception#

    def eval(self, variables: dict):
        return None

    @staticmethod
    def type() -> str:
        return "NULL"


class Id(Simple):
    def __init__(self, token: Token):
        super().__init__(token)
        if token.token_type != TokenType.T_ID:
            raise Exception#

    def id(self):
        return self.token.value

    def eval(self, variables: dict):
        if variables is None:
            raise Exception#
        value = variables.get(self.id())
        if value is None:
            return Error("Error", "", "", 0, 0)#
        return value

    def __repr__(self) -> str:
        return "ID({})".format(self.id())
