from compilation.ast.operations import Node, is_error, is_bool, Error
from compilation.ast.nodes import Bool, Token, TokenType


class Conditional(Node):
    def __init__(self, condition: Node, body: Node, next_cond: Node = None):
        self.condition = condition
        self.body = body
        self.next_cond = next_cond

    def eval(self, variables: dict):
        value = self.condition.eval(variables)
        if is_error(value):
            return value
        if not is_bool(value):
            return Error("Error", "", "", 0, 0)#
        if value:
            return self.body.eval(variables)
        if self.next_cond is not None:
            return self.next_cond.eval(variables)
        return None

    def __repr__(self):
        return "{}({}, {}){}".format(self.type, self.condition, self.body,
                                     "_{}".format(self.next_cond) if self.next_cond is not None else "")

    @staticmethod
    def type() -> str:
        return "CONDITIONAL"


class ElifCond(Conditional):
    def __init__(self, condition: Node, body: Node, next_cond: Conditional = None):
        super().__init__(condition, body, next_cond)

    @staticmethod
    def type() -> str:
        return "ELIF"


class IfCond(Conditional):
    def __init__(self, condition: Node, body: Node, next_cond: ElifCond = None):
        super().__init__(condition, body, next_cond)

    @staticmethod
    def type() -> str:
        return "IF"


class ElseCond(ElifCond):
    def __init__(self, body: Node):
        super().__init__(Bool(Token(TokenType.T_TRUE, -1, -1)), body)

    @staticmethod
    def type() -> str:
        return "ELSE"
