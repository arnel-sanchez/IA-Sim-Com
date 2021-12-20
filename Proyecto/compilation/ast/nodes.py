from compilation.tokens import Token, TokenType
from compilation.errors import Error


class Node:
    def __init__(self, variables: dict):
        self.variables = variables

    def eval(self):
        return None

    def __repr__(self):
        return "NODE()"


class Simple(Node):
    def __init__(self, variables: dict, token: Token):
        super().__init__(variables)
        self.token = token

    def eval(self):
        return self.token.value

    def __repr__(self):
        return "{}({})".format(self.type(), self.eval())

    @staticmethod
    def type() -> str:
        return "SIMPLE"


class String(Simple):
    def __init__(self, variables: dict, token: Token):
        super().__init__(variables, token)
        if token.token_type != TokenType.T_S_VALUE:
            self.token.value = Error("Error", "", "", 0, 0)#

    @staticmethod
    def type() -> str:
        return "STRING"


class Number(Simple):
    def __init__(self, variables: dict, token: Token):
        super().__init__(variables, token)


class Int(Number):
    def __init__(self, variables: dict, token: Token):
        super().__init__(variables, token)
        if token.token_type != TokenType.T_I_VALUE:
            self.token.value = Error("Error", "", "", 0, 0)#

    @staticmethod
    def type() -> str:
        return "INT"


class Double(Number):
    def __init__(self, variables: dict, token: Token):
        super().__init__(variables, token)
        if token.token_type != TokenType.T_D_VALUE:
            self.token.value = Error("Error", "", "", 0, 0)#

    @staticmethod
    def type() -> str:
        return "DOUBLE"


class Bool(Simple):
    def __init__(self, variables: dict, token: Token):
        super().__init__(variables, token)
        if token.token_type != (TokenType.T_TRUE and TokenType.T_FALSE):
            self.token.value = Error("Error", "", "", 0, 0)#

    @staticmethod
    def type() -> str:
        return "BOOL"


class Null(Simple):
    def __init__(self, variables: dict, token: Token):
        super().__init__(variables, token)
        if token.token_type != TokenType.T_NULL:
            self.token.value = Error("Error", "", "", 0, 0)#

    def eval(self):
        return None

    @staticmethod
    def type() -> str:
        return "NULL"


class Id(Simple):
    def __init__(self, variables: dict, token: Token):
        super().__init__(variables, token)
        if token.token_type != TokenType.T_ID:
            self.token.value = Error("Error", "", "", 0, 0)#

    def id(self):
        return self.token.value

    def eval(self):
        value = self.variables.get(self.id())
        if value is None:
            return Error("Error", "", "", 0, 0)#
        return value

    def __repr__(self):
        return "ID({})".format(self.id())
