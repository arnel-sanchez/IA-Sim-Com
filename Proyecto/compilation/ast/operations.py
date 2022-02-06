from compilation.errors import Error, CheckTypesError
from compilation.ast.nodes import Node
from compilation.context import Context


def is_error(value: Error) -> bool:
    return isinstance(value, Error)


def numbertype(type_):
    if type_ == "int" or type_ == "double":
        return True


def is_number(value) -> bool:
    return isinstance(value, int) or isinstance(value, float)


def is_bool(value: bool) -> bool:
    return isinstance(value, bool)


def same_type(value_1, value_2) -> bool:
    return isinstance(value_1, type(value_2))


class Op(Node):
    def __init__(self, right_node: Node):
        self.right_node = right_node

    def eval(self, variables: dict):
        return None

    def __repr__(self) -> str:
        return "{}({})".format(self.type(), self.right_node)

    @staticmethod
    def type() -> str:
        return "OP"


class BinOp(Op):  # @@
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(right_node)
        self.left_node = left_node
        self.token = None

    def validate(self, context: Context):
        validationNodeLeft = self.left_node.validate(context)
        validationNodeRight = self.right_node.validate(context)
        if not isinstance(validationNodeLeft, bool):
            return validationNodeLeft
        if not isinstance(validationNodeRight, bool):
            return validationNodeRight
        return True

    def checktype(self, context: Context):
        typeLeft = self.left_node.checktype(context)
        typeRight = self.right_node.checktype(context)
        if isinstance(typeLeft, CheckTypesError):
            return typeLeft
        if isinstance(typeRight, CheckTypesError):
            return typeRight
        if numbertype(typeLeft) and numbertype(typeRight):
            if typeLeft == typeRight:
                if typeLeft == "int":
                    return "int"
                else:
                    return "double"
            else:
                return "double"
        else:
            return CheckTypesError("You cannot operate arithmetically with tokens that are not of type number", "",
                                   self.token.line, self.token.column)

    def __repr__(self) -> str:
        return "{}({}, {})".format(self.type(), self.left_node, self.right_node)

    @staticmethod
    def type() -> str:
        return "BIN_OP"


class AddOp(BinOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def eval(self, context: Context):
        exprNI = self.left_node.eval(context)
        if isinstance(exprNI, RuntimeError):
            return exprNI
        exprND = self.right_node.eval(context)
        if isinstance(exprND, RuntimeError):
            return exprND

        return exprNI + exprND

    @staticmethod
    def type() -> str:
        return "ADD"


class ArOp(BinOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def type() -> str:
        return "AR_OP"


class SubOp(ArOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def eval(self, context: Context):
        exprNI = self.left_node.eval(context)
        if isinstance(exprNI, RuntimeError):
            return exprNI
        exprND = self.right_node.eval(context)
        if isinstance(exprND, RuntimeError):
            return exprND

        return exprNI - exprND

    @staticmethod
    def type() -> str:
        return "SUB"


class MulOp(BinOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def eval(self, context: Context):
        exprNI = self.left_node.eval(context)
        if isinstance(exprNI, RuntimeError):
            return exprNI
        exprND = self.right_node.eval(context)
        if isinstance(exprND, RuntimeError):
            return exprND
        return exprNI * exprND

    @staticmethod
    def type() -> str:
        return "MUL"


class DivOp(ArOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)
        self.token = None

    def eval(self, context: Context):
        evaluatenoderight = self.right_node.eval(context)
        if isinstance(evaluatenoderight, RuntimeError):
            return evaluatenoderight
        evaluatenodeleft = self.left_node.eval(context)
        if isinstance(evaluatenodeleft, RuntimeError):
            return evaluatenodeleft
        if evaluatenoderight != 0:
            return evaluatenodeleft / evaluatenoderight
        else:
            return RuntimeError("division by zero", "", self.token.line, self.token.column)

    @staticmethod
    def type() -> str:
        return "DIV"


class ModOp(DivOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)
        self.token = None

    def eval(self, context: Context):
        evaluatenoderight = self.right_node.eval(context)
        if isinstance(evaluatenoderight, RuntimeError):
            return evaluatenoderight
        evaluatenodeleft = self.left_node.eval(context)
        if isinstance(evaluatenodeleft, RuntimeError):
            return evaluatenodeleft
        if evaluatenoderight != 0:
            return evaluatenodeleft % evaluatenoderight
        else:
            return RuntimeError("division by zero", "", self.token.line, self.token.column)

    @staticmethod
    def type() -> str:
        return "MOD"


class ExpOp(ArOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def eval(self, context: Context):
        exprNI = self.left_node.eval(context)
        if isinstance(exprNI, RuntimeError):
            return exprNI
        exprND = self.right_node.eval(context)
        if isinstance(exprND, RuntimeError):
            return exprND

        return exprNI ** exprND

    @staticmethod
    def type() -> str:
        return "EXP"


class BoolOp(BinOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def type() -> str:
        return "BOOL_OP"


class AndOp(BoolOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def eval(self, context: Context):
        return self.left_node and self.right_node

    @staticmethod
    def type() -> str:
        return "AND"


class OrOp(BoolOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def eval(self, context: Context):
        return self.left_node or self.right_node

    @staticmethod
    def type() -> str:
        return "OR"


class XorOp(BoolOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def eval(self, context: Context):
        return self.left_node ^ self.right_node

    @staticmethod
    def type() -> str:
        return "XOR"
