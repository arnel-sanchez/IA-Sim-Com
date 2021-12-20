from compilation.errors import Error
from compilation.ast.nodes import Node


def is_error(value):
    return isinstance(value, Error)


def is_number(value):
    return isinstance(value, int) or isinstance(value, float)


def is_bool(value):
    return isinstance(value, bool)


def same_type(value_1, value_2):
    return isinstance(value_1, type(value_2))


class Op(Node):
    def __init__(self, variables: dict, right_node: Node):
        super().__init__(variables)
        self.right_node = right_node

    def eval(self):
        return None

    def __repr__(self):
        return "{}({})".format(self.type(), self.right_node)

    @staticmethod
    def type() -> str:
        return "OP"


class IdOp(Op):
    def __init__(self, variables: dict, number: Node):
        super().__init__(variables, number)

    def eval(self):
        value = self.right_node.eval()
        if is_error(value):
            return value
        return self.operation(value)

    @staticmethod
    def operation(value):
        return value

    @staticmethod
    def type() -> str:
        return "ID_OP"


class RevOp(IdOp):
    def __init__(self, variables: dict, number: Node):
        super().__init__(variables, number)

    @staticmethod
    def operation(value):
        if not is_number(value):
            return Error("Error", "", "", 0, 0)#
        return - value

    @staticmethod
    def type() -> str:
        return "REV"


class NegOp(IdOp):
    def __init__(self, variables: dict, node: Node):
        super().__init__(variables, node)

    @staticmethod
    def operation(value):
        if not is_bool(value):
            return Error("Error", "", "", 0, 0)#
        return not value

    @staticmethod
    def type() -> str:
        return "NEG"


class BinOp(Op):
    def __init__(self, variables: dict, left_node: Node, right_node: Node):
        super().__init__(variables, right_node)
        self.left_node = left_node

    def eval(self):
        left = self.left_node.eval()
        right = self.right_node.eval()
        if is_error(left):
            return left
        if is_error(right):
            return right
        return self.operation(left, right)

    def operation(self, left, right):
        return None

    def __repr__(self):
        return "{}({}, {})".format(self.type(), self.left_node, self.right_node)

    @staticmethod
    def type() -> str:
        return "BIN_OP"


class AddOp(BinOp):
    def __init__(self, variables: dict, left_node: Node, right_node: Node):
        super().__init__(variables, left_node, right_node)

    def operation(self, left, right):
        if not same_type(left, right):
            return Error("Error", "", "", 0, 0)#
        return left + right

    @staticmethod
    def type() -> str:
        return "ADD"


class ArOp(BinOp):
    def __init__(self, variables: dict, left_node: Node, right_node: Node):
        super().__init__(variables, left_node, right_node)

    def operation(self, left, right):
        if not is_number(left):
            return Error("Error", "", "", 0, 0)#
        if not is_number(right):
            return Error("Error", "", "", 0, 0)#
        self.op(left, right)

    @staticmethod
    def op(left, right):
        return None

    @staticmethod
    def type() -> str:
        return "AR_OP"


class SubOp(ArOp):
    def __init__(self, variables: dict, left_node: Node, right_node: Node):
        super().__init__(variables, left_node, right_node)

    @staticmethod
    def op(left, right):
        return left - right

    @staticmethod
    def type() -> str:
        return "SUB"


class MulOp(BinOp):
    def __init__(self, variables: dict, left_node: Node, right_node: Node):
        super().__init__(variables, left_node, right_node)

    def operation(self, left, right):
        return left * right

    @staticmethod
    def type() -> str:
        return "MUL"


class DivOp(ArOp):
    def __init__(self, variables: dict, left_node: Node, right_node: Node):
        super().__init__(variables, left_node, right_node)

    @staticmethod
    def op(left, right):
        if right == 0:
            return Error("Error", "", "", 0, 0)#
        return left / right

    @staticmethod
    def type() -> str:
        return "DIV"


class ModOp(DivOp):
    def __init__(self, variables: dict, left_node: Node, right_node: Node):
        super().__init__(variables, left_node, right_node)

    @staticmethod
    def op(left, right):
        if right == 0:
            return Error("Error", "", "", 0, 0)#
        return left % right

    @staticmethod
    def type() -> str:
        return "MOD"


class ExpOp(ArOp):
    def __init__(self, variables: dict, left_node: Node, right_node: Node):
        super().__init__(variables, left_node, right_node)

    @staticmethod
    def op(left, right):
        return left ** right

    @staticmethod
    def type() -> str:
        return "EXP"


class BoolOp(BinOp):
    def __init__(self, variables: dict, left_node: Node, right_node: Node):
        super().__init__(variables, left_node, right_node)

    def operation(self, left, right):
        if not is_bool(left):
            return Error("Error", "", "", 0, 0)#
        if not is_bool(right):
            return Error("Error", "", "", 0, 0)#
        self.op(left, right)

    @staticmethod
    def op(left, right):
        return None

    @staticmethod
    def type() -> str:
        return "BOOL_OP"


class AndOp(BoolOp):
    def __init__(self, variables: dict, left_node: Node, right_node: Node):
        super().__init__(variables, left_node, right_node)

    @staticmethod
    def op(left, right):
        return left and right

    @staticmethod
    def type() -> str:
        return "AND"


class OrOp(BoolOp):
    def __init__(self, variables: dict, left_node: Node, right_node: Node):
        super().__init__(variables, left_node, right_node)

    @staticmethod
    def op(left, right):
        return left or right

    @staticmethod
    def type() -> str:
        return "OR"


class XorOp(BoolOp):
    def __init__(self, variables: dict, left_node: Node, right_node: Node):
        super().__init__(variables, left_node, right_node)

    @staticmethod
    def op(left, right):
        return left ^ right

    @staticmethod
    def type() -> str:
        return "XOR"
