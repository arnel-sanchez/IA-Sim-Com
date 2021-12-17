from enum import Enum


class VariableType(Enum):
    STRING = 1
    INT = 2
    DOUBLE = 3
    BOOL = 4
    ARRAY = 5


class Variable:
    def __init__(self, variable_type: VariableType, variable_id: str, value):
        self.variable_type = variable_type
        self.variable_id = variable_id
        self.value = value


class MethodType(VariableType):
    VOID = 6


class Method:
    def __init__(self, method_type: MethodType, method_id: str, args: list, body):##Ver que se pone en body
        self.method_type = method_type
        self.method_id = method_id
        self.args = args
