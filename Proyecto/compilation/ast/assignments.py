from compilation.ast.nodes import Node, normaliza
from compilation.context import Context
from compilation.errors import CheckTypesError
from compilation.enums import VariableType


def is_string(value: str) -> bool:
    return isinstance(value, str)


class Assign(Node):
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.expression = None
        self.token = None

    def checktype(self, context: Context):
        checkexpr = self.expression.checktype(context)
        if isinstance(checkexpr, CheckTypesError):
            checkexpr.line = self.token.line
            checkexpr.column = self.token.column
            return checkexpr
        if checkexpr == normaliza(context.gettypevar(self.node_id)):
            return True
        else:
            return CheckTypesError("the expression to be assigned is not of the same type as the variable", "",
                                   self.token.line, self.token.column)

    def eval(self, context: Context):
        return self.expression.eval(context)

    def __repr__(self):
        return "{}_ASSIGN({}, {})".format(self.type(), self.node_id, self.expression)

    @staticmethod
    def type() -> str:
        return "U"


class OpAs(Assign):
    def __init__(self, node_id: str):
        super().__init__(node_id)

    def checktype(self, context: Context):
        checkexpr = self.expression.checktype(context)
        if isinstance(checkexpr, CheckTypesError):
            checkexpr.line = self.token.line
            checkexpr.column = self.token.column
            return checkexpr
        if normaliza(context.gettypevar(self.node_id)) == "int":
            if checkexpr == "int":
                return True
            else:
                return CheckTypesError("the induced type of the expression is different from the type of the variable",
                                       "", self.token.line, self.token.column)
        elif normaliza(context.gettypevar(self.node_id)) == "double":
            if checkexpr == "int" or checkexpr == "double":
                return True
            else:
                return CheckTypesError("The induced type of the expression is not a number", "", self.token.line,
                                       self.token.column)
        else:
            return CheckTypesError("It is incorrect to apply this operation on this type of variables", "",
                                   self.token.line, self.token.column)

    def __repr__(self):
        return "{}_AS({}, {})".format(self.type(), self.node_id, self.expression)

    @staticmethod
    def type() -> str:
        return "OP"


class AddAs(OpAs):
    def __init__(self, node_id: str):
        super().__init__(node_id)

    def eval(self, context: Context):
        if context.variables[self.node_id].value is None:
            return RuntimeError("local variable {} referenced before assignment".format(self.node_id), "",
                                self.token.line, self.token.column)
        evalexpression = self.expression.eval(context)
        if isinstance(evalexpression, RuntimeError):
            return evalexpression
        if context.variables[self.node_id].typevar == VariableType.INT:
            return int(context.variables[self.node_id].value + evalexpression)
        else:
            return float(context.variables[self.node_id].value + evalexpression)

    @staticmethod
    def type() -> str:
        return "ADD"


class ArAs(OpAs):
    def __init__(self, node_id: str):
        super().__init__(node_id)

    @staticmethod
    def type() -> str:
        return "AR"


class SubAs(ArAs):
    def __init__(self, node_id: str):
        super().__init__(node_id)

    def eval(self, context: Context):
        if context.variables[self.node_id].value is None:
            return RuntimeError("local variable {} referenced before assignment".format(self.node_id), "",
                                self.token.line, self.token.column)
        evalexpression = self.expression.eval(context)
        if isinstance(evalexpression, RuntimeError):
            return evalexpression
        if context.variables[self.node_id].typevar == VariableType.INT:
            return int(context.variables[self.node_id].value - evalexpression)
        else:
            return float(context.variables[self.node_id].value - evalexpression)

    @staticmethod
    def type() -> str:
        return "SUB"


class MulAs(OpAs):
    def __init__(self, node_id: str):
        super().__init__(node_id)

    def eval(self, context: Context):
        if context.variables[self.node_id].value is None:
            return RuntimeError("local variable {} referenced before assignment".format(self.node_id), "",
                                self.token.line, self.token.column)
        evalexpression = self.expression.eval(context)
        if isinstance(evalexpression, RuntimeError):
            return evalexpression
        if context.variables[self.node_id].typevar == VariableType.INT:
            return int(context.variables[self.node_id].value * evalexpression)
        else:
            return float(context.variables[self.node_id].value * evalexpression)

    @staticmethod
    def type() -> str:
        return "MUL"


class DivAs(ArAs):
    def __init__(self, node_id: str):
        super().__init__(node_id)

    def eval(self, context: Context):
        if context.variables[self.node_id].value is None:
            return RuntimeError("local variable {} referenced before assignment".format(self.node_id), "",
                                self.token.line, self.token.column)
        nododDivision = self.expression.eval(context)
        if isinstance(nododDivision, RuntimeError):
            return nododDivision
        if nododDivision == 0:
            return RuntimeError("division by zero", "", self.token.line, self.token.column)
        elif context.variables[self.node_id].typevar == VariableType.INT:
            return int(context.variables[self.node_id].value / nododDivision)
        else:
            return float(context.variables[self.node_id].value / nododDivision)

    @staticmethod
    def type() -> str:
        return "DIV"


class ModAs(DivAs):
    def __init__(self, node_id: str):
        super().__init__(node_id)

    def eval(self, context: Context):
        if context.variables[self.node_id].value is None:
            return RuntimeError("local variable {} referenced before assignment".format(self.node_id), "",
                                self.token.line, self.token.column)
        nododDivision = self.expression.eval(context)
        if isinstance(nododDivision, RuntimeError):
            return nododDivision
        if nododDivision == 0:
            return RuntimeError("division by zero", "", self.token.line, self.token.column)
        elif context.variables[self.node_id].typevar == VariableType.INT:
            return int(context.variables[self.node_id].value % nododDivision)
        else:
            return float(context.variables[self.node_id].value % nododDivision)

    @staticmethod
    def type() -> str:
        return "MOD"


class ExpAs(ArAs):
    def __init__(self, node_id: str):
        super().__init__(node_id)

    def checktype(self, context: Context):
        checkexpr = self.expression.checktype(context)
        if isinstance(checkexpr, CheckTypesError):
            checkexpr.line = self.token.line
            checkexpr.column = self.token.column
            return checkexpr
        if normaliza(context.gettypevar(self.node_id)) == "int" or normaliza(
                context.gettypevar(self.node_id)) == "double":
            if checkexpr == "int":
                return True
            else:
                return CheckTypesError("the exponent must be an integer", "", self.token.line, self.token.column)
        else:
            return CheckTypesError("incorrect variable type for power operation", "", self.token.line,
                                   self.token.column)

    def eval(self, context: Context):
        if context.variables[self.node_id].value is None:
            return RuntimeError("local variable {} referenced before assignment".format(self.node_id), "",
                                self.token.line, self.token.column)
        exponente = self.expression.eval(context)
        if isinstance(exponente, RuntimeError):
            return exponente
        if context.variables[self.node_id].typevar == VariableType.INT:
            return int(context.variables[self.node_id].value ** exponente)
        else:
            return float(context.variables[self.node_id].value ** exponente)

    @staticmethod
    def type() -> str:
        return "EXP"


class BoolAs(OpAs):
    def __init__(self, node_id: str):
        super().__init__(node_id)

    def checktype(self, context: Context):
        checkexpr = self.expression.checktype(context)
        if isinstance(checkexpr, CheckTypesError):
            checkexpr.line = self.token.line
            checkexpr.column = self.token.column
            return checkexpr
        if checkexpr == normaliza(context.gettypevar(self.node_id)):
            return True
        else:
            return CheckTypesError("the expression to be assigned is not of the same type as the variable", "",
                                   self.token.line, self.token.column)

    @staticmethod
    def type() -> str:
        return "BOOL"


class AndAs(BoolAs):
    def __init__(self, node_id: str):
        super().__init__(node_id)

    def eval(self, context: Context):
        if context.variables[self.node_id].value is None:
            return RuntimeError("local variable {} referenced before assignment".format(self.node_id), "",
                                self.token.line, self.token.column)
        evalexpression = self.expression.eval(context)
        if isinstance(evalexpression, RuntimeError):
            return evalexpression
        return context.variables[self.node_id].value & evalexpression

    @staticmethod
    def type() -> str:
        return "AND"


class OrAs(BoolAs):
    def __init__(self, node_id: str):
        super().__init__(node_id)

    def eval(self, context: Context):
        if context.variables[self.node_id].value is None:
            return RuntimeError("local variable {} referenced before assignment".format(self.node_id), "",
                                self.token.line, self.token.column)
        evalexpression = self.expression.eval(context)
        if isinstance(evalexpression, RuntimeError):
            return evalexpression
        return context.variables[self.node_id].value | evalexpression

    @staticmethod
    def type() -> str:
        return "OR"


class XorAs(BoolAs):
    def __init__(self, node_id: str):
        super().__init__(node_id)

    def eval(self, context: Context):
        if context.variables[self.node_id].value is None:
            return RuntimeError("local variable {} referenced before assignment".format(self.node_id), "",
                                self.token.line, self.token.column)
        evalexpression = self.expression.eval(context)
        if isinstance(evalexpression, RuntimeError):
            return evalexpression
        return context.variables[self.node_id].value ^ evalexpression

    @staticmethod
    def type() -> str:
        return "XOR"
