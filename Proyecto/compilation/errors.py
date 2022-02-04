
class Error:
    def __init__(self, error_type: str, details: str, file: str, line: int, column: int):
        self.error_type = error_type
        self.details = details
        self.file = file
        self.line = line
        self.column = column

    def __repr__(self):
        return "{} ERROR: '{}', file {}, line {}, column {}".format(self.error_type, self.details, self.file,
                                                                    self.line, self.column)


class UnknownCharacterError(Error):
    def __init__(self, details: str, file: str, line: int, column: int):
        super().__init__("UNKNOWN CHARACTER", details, file, line, column)


class UnexpectedCharacterError(Error):
    def __init__(self, details: str, file: str, line: int, column: int):
        super().__init__("UNEXPECTED CHARACTER", details, file, line, column)


class UnbalancedBracketsError(Error):
    def __init__(self, details: str, file: str, line: int, column: int):
        super().__init__("UNBALANCED BRACKET", details, file, line, column)

class IncorrectCallError(Error):
    def __init__(self, details: str, file: str, line: int, column: int):
        super().__init__("INCORRECT CALL", details, file, line, column)

class CheckTypesError(Error):
    def __init__(self, details: str, file: str, line: int, column: int):
        super().__init__("TYPE ERROR", details, file, line, column)

class RunTimeError(Error):
    def __init__(self, details: str, file: str, line: int, column: int):
        super().__init__("RUNTIME ERROR", details, file, line, column)

#ZeroDivisionError