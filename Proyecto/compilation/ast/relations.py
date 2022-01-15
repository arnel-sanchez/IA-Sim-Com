from compilation.ast.operations import BinOp
from compilation.ast.nodes import Node

class Rel(BinOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def operation(self, left, right) -> bool:
        return same_type(left, right) and self.op(left, right)

    def checktype(self, context):
        if self.right_node==None and self.left_node.checktype(context)=="bool" :
              return True     
        if self.left_node.checktype(context) == self.right_node.checktype(context):
           return True
        return False

    @staticmethod
    def op(left, right) -> bool:
        return False

    @staticmethod
    def type() -> str:
        return "EQ"


class EqRel(Rel):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left, right) -> bool:
        return left == right

    @staticmethod
    def type() -> str:
        return "EQ"


class NeqRel(Rel):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left, right) -> bool:
        return left != right

    @staticmethod
    def type() -> str:
        return "NEQ"


class LessRel(Rel):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left, right) -> bool:
        return left < right

    @staticmethod
    def type() -> str:
        return "LESS"


class LeqRel(Rel):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left, right) -> bool:
        return left <= right

    @staticmethod
    def type() -> str:
        return "LEQ"


class GreatRel(Rel):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left, right) -> bool:
        return left > right

    @staticmethod
    def type() -> str:
        return "GREAT"


class GreqRel(Rel):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left, right) -> bool:
        return left >= right

    @staticmethod
    def type() -> str:
        return "GREQ"
