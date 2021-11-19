from tokens import TokenType, predefine, Token


def tokenize(input_str: str) -> [TokenType]:
    keywords, operators, punctuators = predefine()
    i = 0
    j = 0
    line = 1  #review
    column = 1  #review
    tokens = []
    open_parens = 0
    open_brakes = 0
    open_braces = 0
    while i < len(input_str):
        if input_str[i] == ' ' or input_str[i] == '\t':
            pass
        elif input_str[i] == '\n':
            line += 1
            column = 0
        elif input_str[i] == '\r':
            if i + 1 < len(input_str) and input_str[i + 1] == '\n':
                i += 1
            line += 1
            column = 0
        elif input_str[i] == ';':
            tokens.append(Token(line, column, TokenType.T_SEMICOLON))
        elif input_str[i] == '(':
            open_parens += 1
            tokens.append(Token(line, column, TokenType.T_OPEN_PAREN))
        elif input_str[i] == ')':
            open_parens -= 1
            tokens.append(Token(line, column, TokenType.T_CLOSE_PAREN))
        elif input_str[i] == '[':
            open_brakes += 1
            tokens.append(Token(line, column, TokenType.T_OPEN_BRAKE))
        elif input_str[i] == ']':
            open_brakes -= 1
            tokens.append(Token(line, column, TokenType.T_CLOSE_BRAKE))
        elif input_str[i] == '{':
            open_braces += 1
            tokens.append(Token(line, column, TokenType.T_OPEN_BRACE))
        elif input_str[i] == '}':
            open_braces -= 1
            tokens.append(Token(line, column, TokenType.T_CLOSE_BRACE))
        elif input_str[i] == '#' or input_str[i] == '\"':
            i = comment_string(input_str, i, line, column, tokens)
        elif input_str[i].isnumeric():
            i = number(input_str, i, j, line, column, tokens)
        elif input_str[i].isalpha() or input_str[i] == "_":
            i = alpha(keywords, input_str, i, line, column, tokens)
        else:
            opt = operators.get(input_str[i])
            if opt:
                i = operator(operators, input_str, i, line, column, tokens, opt)
            else:
                pct = punctuators.get(input_str[i])
                if pct:
                    tokens.append(Token(line, column, pct))
                else:
                    tokens.append(Token(line, column, TokenType.T_INVALID, input_str[i]))
                    raise Exception("UNKNOWN CHARACTER")  #ERROR
        i += 1
        column += i - j
        j = i
    if open_parens > 0:
        raise Exception("PARENTHESIS UNBALANCED")  #ERROR
    if open_braces > 0:
        raise Exception("BRACES UNBALANCED")  #ERROR
    return tokens


def comment_string(input_str: str, i: int, line: int, column: int, tokens: [Token]) -> int:
    char = input_str[i]
    token = ""
    while i < len(input_str):
        i += 1
        if input_str[i] == char:
            break
        token += input_str[i]
    tokens.append(Token(line, column, TokenType.T_COMMENT if char == '#' else TokenType.T_STRING, token))
    return i


def number(input_str: str, i: int, j: int, line: int, column: int, tokens: [Token]) -> int:
    token = ""
    double = False
    while i < len(input_str) and (input_str[i].isnumeric() or input_str[i] == '.'):
        token += input_str[i]
        if input_str[i] == '.':
            if double:
                raise Exception("UNEXPECTED CHARACTER: line {}, column {}".format(line, column + i - j))  #ERROR
            double = True
        i += 1
    if i < len(input_str) and input_str[i].isalpha():
        raise Exception("UNEXPECTED CHARACTER: line {}, column {}".format(line, column + i - j))  #ERROR
    if double:
        tokens.append(Token(line, column, TokenType.T_DOUBLE, float(token)))
    else:
        tokens.append(Token(line, column, TokenType.T_INT, int(token)))
    return i - 1


def alpha(keywords: dict, input_str: str, i: int, line: int, column: int, tokens: [Token]) -> int:
    token = ""
    while i < len(input_str) and (input_str[i].isalpha() or input_str[i].isnumeric() or input_str[i] == "_"):
        token += input_str[i]
        i += 1
    keyword = keywords.get(token)
    if keyword:
        tokens.append(Token(line, column, keyword))
    else:
        tokens.append(Token(line, column, TokenType.T_ID, token))
    return i - 1


def operator(operators: dict, input_str: str, i: int, line: int, column: int, tokens: [Token], opt: TokenType) -> int:
    token = input_str[i]
    while i < len(input_str):
        token += input_str[i + 1]
        comp_operator = operators.get(token)
        if not comp_operator:
            break
        opt = comp_operator
        i += 1
    tokens.append(Token(line, column, opt))
    return i - 1
