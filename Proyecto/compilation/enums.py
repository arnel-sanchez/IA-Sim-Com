from enum import Enum


class Region(Enum):
    R_IF = 0
    R_ELIF = 1
    R_ELSE = 2
    R_WHILE = 3
    R_METHOD = 4
    R_TYPE = 5


class EstadoDAST(Enum):
    EnProgram = 0
    EnAsignacion = 1
    EnWhile = 2
    EnCondicionIf = 3
    EnFuncion = 4
    EnArgsdFuncion = 8
    EnExpresion = 5
    EnTipoEspecial = 6
    EnExpresionAssign = 7
    EnRedefinition = 9
    Condicion = 10
    LlamadoAfuncion = 11
    CreandoArray = 12


class VariableType(Enum):
    STRING = 0
    INT = 1
    DOUBLE = 2
    BOOL = 3
    ARRAY = 4


class MethodType(Enum):
    VOID = 0
    STRING = 1
    INT = 2
    DOUBLE = 3
    BOOL = 4
    ARRAY = 5
