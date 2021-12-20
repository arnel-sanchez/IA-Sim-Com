from compilation.ast.operations import Node, is_error, is_bool, Error


class Conditional(Node):
    def __init__(self, variables: dict, condition: Node, body: Node, next_cond: Node = None):
        super().__init__(variables)
        self.condition = condition
        self.body = body
        self.next_cond = next_cond

    def eval(self):
        value = self.condition.eval()
        if is_error(value):
            return value
        if not is_bool(value):
            return Error("Error", "", "", 0, 0)#
        if value:
            return self.body.eval()
        if self.next_cond is not None:
            return self.next_cond.eval()
        return Error("Error", "", "", 0, 0)#

    def __repr__(self):
        return "{}({}, {}){}".format(self.type, self.condition, self.body,
                                     "_{}".format(self.next_cond) if self.next_cond is not None else "")

    @staticmethod
    def type() -> str:
        return "CONDITIONAL"


class IfCond(Conditional):
    def __init__(self, variables: dict, condition: Node, body: Node, next_cond: Conditional):
        super().__init__(variables, condition, body, next_cond)

    @staticmethod
    def type() -> str:
        return "IF"


class ElifCond(Conditional):
    def __init__(self, variables: dict, condition: Node, body: Node, next_cond: Conditional):
        super().__init__(variables, condition, body, next_cond)

    @staticmethod
    def type() -> str:
        return "ELIF"


class ElseCond(Conditional):
    def __init__(self, variables: dict, condition: Node, body: Node):
        super().__init__(variables, condition, body)

    @staticmethod
    def type() -> str:
        return "ELSE"
