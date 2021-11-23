from compilation.tokens import Token, TokenType


def is_number(token: Token) -> bool:
    return token.token_type == TokenType.T_INT or token.token_type == TokenType.T_DOUBLE


def are_numbers(token_1: Token, token_2: Token) -> bool:
    return is_number(token_1) and is_number(token_2)


def is_string(token: Token) -> bool:
    return token.token_type == TokenType.T_STRING


def are_bool(token_1: Token, token_2: Token) -> bool:
    return token_1.token_type == token_2.token_type == TokenType.T_BOOL


def id_op(token: Token):
    if is_number(token):
        return token.value
    raise Exception()


def neg_op(token: Token):
    if is_number(token):
        return - token.value
    raise Exception()


def log_neg_op(token: Token) -> bool:
    if token.token_type == TokenType.T_BOOL:
        return not token.value
    raise Exception()


def add_op(token_1: Token, token_2: Token):
    if are_numbers(token_1, token_2) or (is_string(token_1) and is_string(token_2)):
        return token_1.value + token_2.value
    else:
        raise Exception()


def sub_op(token_1: Token, token_2: Token):
    if are_numbers(token_1, token_2):
        return token_1.value - token_2.value
    else:
        raise Exception()


def mul_op(token_1: Token, token_2: Token):
    if are_numbers(token_1, token_2) or (is_string(token_1) and token_2.token_type == TokenType.T_INT) or \
            (token_1.token_type == TokenType.T_INT and is_string(token_2)):
        return token_1.value * token_2.value
    else:
        raise Exception()


def exp_op(token_1: Token, token_2: Token):
    if are_numbers(token_1, token_2):
        return token_1.value ** token_2.value
    else:
        raise Exception()


def div_op(token_1: Token, token_2: Token):
    if are_numbers(token_1, token_2):
        if token_2.value == 0:
            raise Exception
        return token_1.value / token_2.value
    else:
        raise Exception()


def mod_op(token_1: Token, token_2: Token):
    if are_numbers(token_1, token_2):
        if token_2.value == 0:
            raise Exception
        return token_1.value % token_2.value
    else:
        raise Exception()


def eq_rel(token_1: Token, token_2: Token) -> bool:
    return token_1.value == token_2.value


def neq_rel(token_1: Token, token_2: Token) -> bool:
    return token_1.value != token_2.value


def less_rel(token_1: Token, token_2: Token) -> bool:
    if are_numbers(token_1, token_2):
        return token_1.value < token_2.value
    else:
        raise Exception()


def leq_rel(token_1: Token, token_2: Token) -> bool:
    if are_numbers(token_1, token_2):
        return token_1.value <= token_2.value
    else:
        raise Exception()


def great_rel(token_1: Token, token_2: Token) -> bool:
    if are_numbers(token_1, token_2):
        return token_1.value > token_2.value
    else:
        raise Exception()


def greq_rel(token_1: Token, token_2: Token) -> bool:
    if are_numbers(token_1, token_2):
        return token_1.value >= token_2.value
    else:
        raise Exception()


def and_op(token_1: Token, token_2: Token) -> bool:
    if are_bool(token_1, token_2):
        return token_1.value and token_2.value
    else:
        raise Exception()


def or_op(token_1: Token, token_2: Token) -> bool:
    if are_bool(token_1, token_2):
        return token_1.value or token_2.value
    else:
        raise Exception()


def xor_op(token_1: Token, token_2: Token) -> bool:
    if are_bool(token_1, token_2):
        return not token_2.value if token_1.value else token_2.value
    else:
        raise Exception()
