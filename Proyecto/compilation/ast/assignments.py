from compilation.ast.operations import Node, is_error, is_number, is_bool
from compilation.ast.nodes import Id, Error
from compilation.variables import VariableType


def is_string(value: str) -> bool:
    return isinstance(value, str)


class Assign(Node):
    def __init__(self, variables: dict, id_node: Id, expression: Node):
        super().__init__(variables)
        self.id_node = id_node
        self.expression = expression

    def eval(self, variables: dict):
        var_id = self.id_node.id()
        if not variables.keys().__contains__(var_id):
            return Error("Error", "", "", 0, 0)#
        value = self.expression.eval(variables)
        if is_error(value):
            return value
        return self.review(variables, var_id, value)

    @staticmethod
    def review(variables: dict, var_id: str, value):
        variables[var_id] = value
        return value

    def __repr__(self):
        return "{}_ASSIGN({})".format(self.type(), self.id_node)

    @staticmethod
    def type() -> str:
        return "U"


class StringAssign(Assign):
    def __init__(self, variables: dict, id_node: Id, expression: Node):
        super().__init__(variables, id_node, expression)

    @staticmethod
    def review(variables: dict, var_id: str, value: str):
        if variables[var_id].var_type != VariableType.STRING:
            raise Exception#
        if not is_string(value):
            return Error("Error", "", "", 0, 0)#
        return super().review(variables, var_id, value)

    @staticmethod
    def type() -> str:
        return "S"


class IntAssign(Assign):
    def __init__(self, variables: dict, id_node: Id, expression: Node):
        super().__init__(variables, id_node, expression)

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
    def __init__(self, variables: dict, id_node: Id, expression: Node):
        super().__init__(variables, id_node, expression)

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
    def __init__(self, variables: dict, id_node: Id, expression: Node):
        super().__init__(variables, id_node, expression)

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
    def __init__(self, variables: dict, id_node: Id, expression: Node):
        super().__init__(variables, id_node, expression)

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
