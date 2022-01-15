from compilation.ast.nodes import Node ,Error

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

class BinOp(Op):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(right_node)
        self.left_node = left_node

    def validate(self,context:Context):
        return self.left_node.validate(context) and self.right_node.validate(context)

    def checktype(self,context:Context):
        typeLeft= self.left_node.checktype(context)
        typeRight=self.right_node.checktype(context)
        if is_number(typeLeft) and is_number(typeRight):
           if typeLeft==typeRight :
             if typeLeft=="int":
                return "int"
             else :
                 return "double"
           else :
               return "double"

    def eval(self, variables: dict):
        left = self.left_node.eval(variables)
        right = self.right_node.eval(variables)
        if is_error(left):
            return left
        if is_error(right):
            return right
        return self.operation(left, right)

    def operation(self, left, right):
        return None

    def __repr__(self) -> str:
        return "{}({}, {})".format(self.type(), self.left_node, self.right_node)

    @staticmethod
    def type() -> str:
        return "BIN_OP"


class AddOp(BinOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def operation(self, left, right):
        if not same_type(left, right):
            return Error("Error", "", "", 0, 0)#
        return left + right

    @staticmethod
    def type() -> str:
        return "ADD"


class ArOp(BinOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

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
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left, right):
        return left - right

    @staticmethod
    def type() -> str:
        return "SUB"

class MulOp(BinOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def operation(self, left, right):
        return left * right

    @staticmethod
    def type() -> str:
        return "MUL"

class DivOp(ArOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left, right):
        if right == 0:
            return Error("Error", "", "", 0, 0)#
        return left / right

    @staticmethod
    def type() -> str:
        return "DIV"


class ModOp(DivOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)
            

    @staticmethod
    def op(left, right):
        if right == 0:
            return Error("Error", "", "", 0, 0)#
        return left % right

    @staticmethod
    def type() -> str:
        return "MOD"

class ExpOp(ArOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left, right):
        return left ** right

    @staticmethod
    def type() -> str:
        return "EXP"


class BoolOp(BinOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def operation(self, left, right):
        if not is_bool(left):
            return Error("Error", "", "", 0, 0)#
        if not is_bool(right):
            return Error("Error", "", "", 0, 0)#
        self.op(left, right)

    @staticmethod
    def op(left: bool, right: bool) -> bool:
        return False

    @staticmethod
    def type() -> str:
        return "BOOL_OP"


class AndOp(BoolOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left: bool, right: bool) -> bool:
        return left and right

    @staticmethod
    def type() -> str:
        return "AND"


class OrOp(BoolOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left: bool, right: bool) -> bool:
        return left or right

    @staticmethod
    def type() -> str:
        return "OR"


class XorOp(BoolOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left: bool, right: bool) -> bool:
        return left ^ right

    @staticmethod
    def type() -> str:
        return "XOR"