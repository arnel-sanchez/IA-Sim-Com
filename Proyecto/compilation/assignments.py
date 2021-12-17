from compilation.tokens import Token, TokenType
from compilation.variables import Variable, VariableType


def var_action(init: bool, variables: dict, variable_type: VariableType, token_id: Token, value):
    types = dict([(VariableType.STRING, str), (VariableType.INT, int), (VariableType.DOUBLE, float),
                  (VariableType.BOOL, bool), (VariableType.ARRAY, list)])
    if token_id.token_type != TokenType.T_ID:
        raise Exception()  #error: invalid token type
    if init ^ variables.keys().__contains__(token_id.value):
        raise Exception()  #error: existing id (if init), not existing (if not init)
    if type(value) is not types[variable_type]:
        raise Exception()  #error: incorrect type
    variables[token_id] = Variable(variable_type, token_id.value, value)


def var_init(variables: dict, variable_type: VariableType, token_id: Token, value):
    var_action(True, variables, variable_type, token_id, value)


def string_init(variables: dict, token_id: Token, value):
    var_init(variables, VariableType.STRING, token_id, value)


def int_init(variables: dict, token_id: Token, value):
    var_init(variables, VariableType.INT, token_id, value)


def double_init(variables: dict, token_id: Token, value):
    var_init(variables, VariableType.DOUBLE, token_id, value)


def bool_init(variables: dict, token_id: Token, value):
    var_init(variables, VariableType.BOOL, token_id, value)


def array_init(variables: dict, token_id: Token, value):
    var_init(variables, VariableType.ARRAY, token_id, value)


def var_update(variables: dict, variable_type: VariableType, token_id: Token, value):
    var_action(False, variables, variable_type, token_id, value)


def string_update(variables: dict, token_id: Token, value):
    var_update(variables, VariableType.STRING, token_id, value)


def int_update(variables: dict, token_id: Token, value):
    var_update(variables, VariableType.INT, token_id, value)


def double_update(variables: dict, token_id: Token, value):
    var_update(variables, VariableType.DOUBLE, token_id, value)


def bool_update(variables: dict, token_id: Token, value):
    var_update(variables, VariableType.BOOL, token_id, value)


def array_update(variables: dict, token_id: Token, value):
    var_update(variables, VariableType.ARRAY, token_id, value)
