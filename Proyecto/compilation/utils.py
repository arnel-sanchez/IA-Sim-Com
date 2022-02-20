from enum import Enum

from compilation.tokens import Token, TokenType


def split_lines(tokens: [Token]) -> [[TokenType]]:
    t_pointer = 0
    current_line = []
    lines = []
    while t_pointer < len(tokens):
        if tokens[t_pointer].token_type in [TokenType.T_IF, TokenType.T_ELIF, TokenType.T_ELSE, TokenType.T_WHILE,
                                            TokenType.T_METHOD, TokenType.T_RIDER, TokenType.T_BIKE,
                                            TokenType.T_ENVIRONMENT]:
            t_pointer = loop(tokens, t_pointer, current_line, TokenType.T_OPEN_BRACE)
        elif tokens[t_pointer].token_type == TokenType.T_CLOSE_BRACE:
            current_line = [tokens[t_pointer]]
            t_pointer += 1
            if t_pointer < len(tokens) and (tokens[t_pointer].token_type == TokenType.T_ELIF or
                                            tokens[t_pointer].token_type == TokenType.T_ELSE):
                t_pointer = loop(tokens, t_pointer, current_line, TokenType.T_OPEN_BRACE)
        else:
            t_pointer = loop(tokens, t_pointer, current_line, TokenType.T_SEMICOLON)
        lines.append(current_line)
        current_line = []
    return lines


def loop(tokens: [Token], t_pointer: int, current_line: [Token], comparator: TokenType) -> int:
    while t_pointer < len(tokens):
        current_line.append(tokens[t_pointer])
        if tokens[t_pointer].token_type == comparator:
            return t_pointer + 1
        t_pointer += 1
    return t_pointer


class Region(Enum):
    R_IF = 0
    R_ELIF = 1
    R_ELSE = 2
    R_WHILE = 3
    R_METHOD = 4
    R_TYPE = 5
