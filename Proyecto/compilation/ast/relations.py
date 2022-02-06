from compilation.ast.operations import BinOp, same_type
from compilation.ast.nodes import Node
from compilation.context import Context
from compilation.errors import CheckTypesError


class Rel(BinOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def checktype(self, context):
        checkexpr1 = self.left_node.checktype(context)
        if isinstance(checkexpr1, CheckTypesError):
            return checkexpr1
        checkexpr2 = self.right_node.checktype(context)
        if isinstance(checkexpr2, CheckTypesError):
            return checkexpr2
        if checkexpr1 == checkexpr2:
            return True
        return CheckTypesError("cannot compare expressions with different types", "", "", "")

    @staticmethod
    def type() -> str:
        return "EQ"


class EqRel(Rel):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def eval(self, context: Context):
        exprNI = self.left_node.eval(context)
        if isinstance(exprNI, RuntimeError):
            return exprNI
        exprND = self.right_node.eval(context)
        if isinstance(exprND, RuntimeError):
            return exprND

        if exprNI == exprND:
            return True
        else:
            return False

    @staticmethod
    def type() -> str:
        return "EQ"


class NeqRel(Rel):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def eval(self, context: Context):
        exprNI = self.left_node.eval(context)
        if isinstance(exprNI, RuntimeError):
            return exprNI
        exprND = self.right_node.eval(context)
        if isinstance(exprND, RuntimeError):
            return exprND

        if exprNI != exprND:
            return True
        else:
            return False

    @staticmethod
    def type() -> str:
        return "NEQ"


class LessRel(Rel):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def eval(self, context: Context):
        exprNI = self.left_node.eval(context)
        if isinstance(exprNI, RuntimeError):
            return exprNI
        exprND = self.right_node.eval(context)
        if isinstance(exprND, RuntimeError):
            return exprND

        if exprNI < exprND:
            return True
        else:
            return False

    @staticmethod
    def type() -> str:
        return "LESS"


class LeqRel(Rel):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def eval(self, context: Context):
        exprNI = self.left_node.eval(context)
        if isinstance(exprNI, RuntimeError):
            return exprNI
        exprND = self.right_node.eval(context)
        if isinstance(exprND, RuntimeError):
            return exprND

        if exprNI <= exprND:
            return True
        else:
            return False

    @staticmethod
    def type() -> str:
        return "LEQ"


class GreatRel(Rel):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def eval(self, context: Context):
        exprNI = self.left_node.eval(context)
        if isinstance(exprNI, RuntimeError):
            return exprNI
        exprND = self.right_node.eval(context)
        if isinstance(exprND, RuntimeError):
            return exprND

        if exprNI > exprND:
            return True
        else:
            return False

    @staticmethod
    def type() -> str:
        return "GREAT"


class GreqRel(Rel):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def eval(self, context: Context):
        exprNI = self.left_node.eval(context)
        if isinstance(exprNI, RuntimeError):
            return exprNI
        exprND = self.right_node.eval(context)
        if isinstance(exprND, RuntimeError):
            return exprND

        if exprNI >= exprND:
            return True
        else:
            return False

    @staticmethod
    def type() -> str:
        return "GREQ"
