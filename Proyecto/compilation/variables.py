from enum import Enum


class VariableType(Enum):
    STRING = 1
    INT = 2
    DOUBLE = 3
    BOOL = 4
    ARRAY = 5


class Variable:
    def __init__(self, var_type: VariableType, var_id: str, value):
        self.type = var_type
        self.id = var_id
        self.value = value


class MethodType(VariableType):
    VOID = 6


class Method:
    def __init__(self, method_type: MethodType, method_id: str, args: list, body):##Ver que se pone en body
        self.type = method_type
        self.id = method_id
        self.args = args
        self.body = body
