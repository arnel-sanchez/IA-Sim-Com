from compilation.ast.nodes import Node, Id, Error
from compilation.variables import Variable, VariableType, Method, MethodType
from simulation.motorcycle import Motorcycle
from simulation.rider import Rider


class Init(Node):
    def __init__(self, id_node: Id):
        self.id_node = id_node

    def eval(self, variables: dict):
        var_id = self.id_node.id()
        if variables.keys().__contains__(var_id):
            return Error("Error", "", "", 0, 0)#
        variables[var_id] = self.default(var_id)
        return self.id_node

    @staticmethod
    def default(var_id: str):
        return None

    def __repr__(self) -> str:
        return "{}_INIT({})".format(self.type(), self.id_node)

    @staticmethod
    def type() -> str:
        return "U"


class StringInit(Init):
    def __init__(self, id_node: Id):
        super().__init__(id_node)

    @staticmethod
    def default(var_id: str) -> Variable:
        return Variable(var_id, VariableType.STRING, "")

    @staticmethod
    def type() -> str:
        return "S"


class IntInit(Init):
    def __init__(self, id_node: Id):
        super().__init__(id_node)

    @staticmethod
    def default(var_id: str) -> Variable:
        return Variable(var_id, VariableType.INT, 0)

    @staticmethod
    def type() -> str:
        return "I"


class DoubleInit(Init):
    def __init__(self, id_node: Id):
        super().__init__(id_node)

    @staticmethod
    def default(var_id: str) -> Variable:
        return Variable(var_id, VariableType.DOUBLE, 0.0)

    @staticmethod
    def type() -> str:
        return "D"


class BoolInit(Init):
    def __init__(self, id_node: Id):
        super().__init__(id_node)

    @staticmethod
    def default(var_id: str) -> Variable:
        return Variable(var_id, VariableType.BOOL, True)

    @staticmethod
    def type() -> str:
        return "B"


class ArrayInit(Init):
    def __init__(self, id_node: Id):
        super().__init__(id_node)

    @staticmethod
    def default(var_id: str) -> Variable:
        return Variable(var_id, VariableType.ARRAY, [])

    @staticmethod
    def type() -> str:
        return "A"


class MethodInit(Init):
    def __init__(self, id_node: Id):
        super().__init__(id_node)

    @staticmethod
    def default(method_id: str) -> Method:
        return Method(method_id, MethodType.VOID, [])

    @staticmethod
    def type() -> str:
        return "M"


class StringMInit(MethodInit):
    def __init__(self, id_node: Id):
        super().__init__(id_node)

    @staticmethod
    def default(method_id: str) -> Method:
        return Method(method_id, MethodType.STRING, [])

    @staticmethod
    def type() -> str:
        return "S_M"


class IntMInit(MethodInit):
    def __init__(self, id_node: Id):
        super().__init__(id_node)

    @staticmethod
    def default(method_id: str) -> Method:
        return Method(method_id, MethodType.INT, [])

    @staticmethod
    def type() -> str:
        return "I_M"


class DoubleMInit(MethodInit):
    def __init__(self, id_node: Id):
        super().__init__(id_node)

    @staticmethod
    def default(method_id: str) -> Method:
        return Method(method_id, MethodType.DOUBLE, [])

    @staticmethod
    def type() -> str:
        return "D_M"


class BoolMInit(MethodInit):
    def __init__(self, id_node: Id):
        super().__init__(id_node)

    @staticmethod
    def default(method_id: str) -> Method:
        return Method(method_id, MethodType.BOOL, [])

    @staticmethod
    def type() -> str:
        return "B_M"


class ArrayMInit(MethodInit):
    def __init__(self, id_node: Id):
        super().__init__(id_node)

    @staticmethod
    def default(method_id: str) -> Method:
        return Method(method_id, MethodType.ARRAY, [])

    @staticmethod
    def type() -> str:
        return "A_M"




class TypeInit(Init):
    def __init__(self, id_node: Id):
        super().__init__(id_node)

    @staticmethod
    def default(type_id: str):
        return None

    @staticmethod
    def type() -> str:
        return "T"


class MotoInit(TypeInit):
    def __init__(self, id_node: Id):
        super().__init__(id_node)

    @staticmethod
    def default(type_id: str) -> Motorcycle:
        return Motorcycle()

    @staticmethod
    def type() -> str:
        return "MOTO"


class RiderInit(Init):
    def __init__(self, id_node: Id):
        super().__init__(id_node)

    @staticmethod
    def default(type_id: str) -> Rider:
        return Rider()

    @staticmethod
    def type() -> str:
        return "RIDER"
