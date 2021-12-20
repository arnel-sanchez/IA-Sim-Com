from compilation.ast.operations import BinOp, same_type
from compilation.ast.nodes import Node


class Rel(BinOp):
    def __init__(self, variables: dict, left_node: Node, right_node: Node):
        super().__init__(variables, left_node, right_node)

    def operation(self, left, right):
        return same_type(left, right) and self.op(left, right)

    @staticmethod
    def op(left, right):
        return False

    @staticmethod
    def type() -> str:
        return "EQ"


class EqRel(Rel):
    def __init__(self, variables: dict, left_node: Node, right_node: Node):
        super().__init__(variables, left_node, right_node)

    @staticmethod
    def op(left, right):
        return left == right

    @staticmethod
    def type() -> str:
        return "EQ"


class NeqRel(Rel):
    def __init__(self, variables: dict, left_node: Node, right_node: Node):
        super().__init__(variables, left_node, right_node)

    @staticmethod
    def op(left, right):
        return left != right

    @staticmethod
    def type() -> str:
        return "NEQ"


class LessRel(Rel):
    def __init__(self, variables: dict, left_node: Node, right_node: Node):
        super().__init__(variables, left_node, right_node)

    @staticmethod
    def op(left, right):
        return left < right

    @staticmethod
    def type() -> str:
        return "LESS"


class LeqRel(Rel):
    def __init__(self, variables: dict, left_node: Node, right_node: Node):
        super().__init__(variables, left_node, right_node)

    @staticmethod
    def op(left, right):
        return left <= right

    @staticmethod
    def type() -> str:
        return "LEQ"


class GreatRel(Rel):
    def __init__(self, variables: dict, left_node: Node, right_node: Node):
        super().__init__(variables, left_node, right_node)

    @staticmethod
    def op(left, right):
        return left > right

    @staticmethod
    def type() -> str:
        return "GREAT"


class GreqRel(Rel):
    def __init__(self, variables: dict, left_node: Node, right_node: Node):
        super().__init__(variables, left_node, right_node)

    @staticmethod
    def op(left, right):
        return left >= right

    @staticmethod
    def type() -> str:
        return "GREQ"
