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
