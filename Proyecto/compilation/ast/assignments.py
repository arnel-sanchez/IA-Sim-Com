from compilation.ast.nodes import Node, Id, Error
from compilation.variables import VariableType
from compilation.ast.operations import is_error, is_number, is_bool, same_type
from compilation.ast.complex import Expression, normaliza
from compilation.context import Context


def is_string(value: str) -> bool:
    return isinstance(value, str)


class Assign(Node):
    def __init__(self, id_node: Id, expression: Expression):
        self.id_node = id_node
        self.expression = expression

    def validate(self, variables: dict):
        var_id = self.id_node.id()
        if not variables.keys().__contains__(var_id):
            return Error("Error", "", "", 0, 0)#
        return self.review(variables, var_id)

    def review(self, variables: dict, var_id: str):
        return self.expression.validate(variables)

    def eval(self, variables: dict):
        variables[self.id_node.id()] = self.expression.eval(variables)

    def __repr__(self):
        return "{}_ASSIGN({}, {})".format(self.type(), self.id_node, self.expression)

    @staticmethod
    def type() -> str:
        return "U"


class StringAssign(Assign):
    def __init__(self, id_node: Id, expression: Expression):
        super().__init__(id_node, expression)

    def review(self, variables: dict, var_id: str, value):
        if variables[var_id].var_type != VariableType.STRING:
            return Error("Error", "", "", 0, 0)#
        if not is_string(value):
            return Error("Error", "", "", 0, 0)#
        return super().review(variables, var_id, value)

    @staticmethod
    def type() -> str:
        return "S"


class IntAssign(Assign):
    def __init__(self, id_node: Id, expression: Node):
        super().__init__(id_node, expression)

    @staticmethod
    def review(variables: dict, var_id: str, value):
        if variables[var_id].var_type != VariableType.INT:
            raise Exception#
        if not is_number(value):
            return Error("Error", "", "", 0, 0)#
        return super().review(variables, var_id, int(value))

    @staticmethod
    def type() -> str:
        return "I"


class DoubleAssign(Assign):
    def __init__(self, id_node: Id, expression: Node):
        super().__init__(id_node, expression)

    @staticmethod
    def review(variables: dict, var_id: str, value):
        if variables[var_id].var_type != VariableType.DOUBLE:
            raise Exception#
        if not is_number(value):
            return Error("Error", "", "", 0, 0)#
        return super().review(variables, var_id, float(value))

    @staticmethod
    def type() -> str:
        return "D"


class BoolAssign(Assign):
    def __init__(self, id_node: Id, expression: Node):
        super().__init__(id_node, expression)

    @staticmethod
    def review(variables: dict, var_id: str, value):
        if variables[var_id].var_type != VariableType.DOUBLE:
            raise Exception#
        if not is_bool(value):
            return Error("Error", "", "", 0, 0)#
        return super().review(variables, var_id, value)

    @staticmethod
    def type() -> str:
        return "D"


class ArrayAssign(Assign):
    def __init__(self, id_node: Id, expression: Node):
        super().__init__(id_node, expression)

    @staticmethod
    def review(variables: dict, var_id: str, value):
        if variables[var_id].var_type != VariableType.DOUBLE:
            raise Exception#
        if not isinstance(value, list):
            return Error("Error", "", "", 0, 0)#
        return super().review(variables, var_id, value)

    @staticmethod
    def type() -> str:
        return "D"


class OpAs(Assign):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    def checktype(self,context:Context):
        
        if self.expression.checktype(context) == normaliza(context.gettypevar(self.idnode)):
            return True
        else :
            return False

    def __repr__(self):
        return "{}_AS({}, {})".format(self.type(), self.id_node, self.expression)

    @staticmethod
    def type() -> str:
        return "OP"


class AddAs(OpAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    @staticmethod
    def review(variables: dict, var_id: str, value):
        if not same_type(variables[var_id], value):
            raise Exception#
        variables[var_id] += value
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "ADD"


class ArAs(OpAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    def review(self, variables: dict, var_id: str, value):
        if not is_number(variables[var_id]):
            return Error("Error", "", "", 0, 0)  #
        if not is_number(value):
            return Error("Error", "", "", 0, 0)  #
        return self.operation(variables, var_id, value)

    @staticmethod
    def operation(variables: dict, var_id: str, value):
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "AR"


class SubAs(ArAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    @staticmethod
    def operation(variables: dict, var_id: str, value):
        variables[var_id] -= value
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "SUB"


class MulAs(OpAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    @staticmethod
    def review(variables: dict, var_id: str, value):
        variables[var_id] *= value
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "MUL"


class DivAs(ArAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    @staticmethod
    def operation(variables: dict, var_id: str, value):
        if value == 0:
            return Error("Error", "", "", 0, 0)#
        variables[var_id] /= value
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "DIV"


class ModAs(DivAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    @staticmethod
    def operation(variables: dict, var_id: str, value):
        if value == 0:
            return Error("Error", "", "", 0, 0)#
        variables[var_id] %= value
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "MOD"


class ExpAs(ArAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    @staticmethod
    def operation(variables: dict, var_id: str, value):
        variables[var_id] **= value
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "EXP"


class BoolAs(OpAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    def operation(self, variables: dict, var_id: str, value):
        if not is_bool(variables[var_id]):
            return Error("Error", "", "", 0, 0)#
        if not is_bool(value):
            return Error("Error", "", "", 0, 0)#
        return self.op(variables, var_id, value)

    @staticmethod
    def op(variables: dict, var_id: str, value):
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "BOOL"


class AndAs(BoolAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    @staticmethod
    def op(variables: dict, var_id: str, value):
        variables[var_id] &= value
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "AND"


class OrAs(BoolAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    @staticmethod
    def op(variables: dict, var_id: str, value):
        variables[var_id] |= value
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "OR"


class XorAs(BoolAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    @staticmethod
    def op(variables: dict, var_id: str, value):
        variables[var_id] ^= value
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "XOR"
