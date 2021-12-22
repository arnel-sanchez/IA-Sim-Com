from enum import Enum


class VariableType(Enum):
    STRING = 0
    INT = 1
    DOUBLE = 2
    BOOL = 3
    ARRAY = 4


class Variable:
    def __init__(self, var_id: str, var_type: VariableType, value):
        self.id = var_id
        self.type = var_type
        self.value = value


class MethodType(Enum):
    VOID = 0
    STRING = 1
    INT = 2
    DOUBLE = 3
    BOOL = 4
    ARRAY = 5


class Method:
    def __init__(self, method_id: str, method_type: MethodType, args: list, body=None):##Ver que se pone en body
        self.id = method_id
        self.type = method_type
        self.args = args
        self.body = body
