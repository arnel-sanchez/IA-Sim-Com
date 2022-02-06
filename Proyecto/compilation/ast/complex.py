from compilation.enums import VariableType, MethodType
from compilation.ast.nodes import Node, TokenType, Token
from compilation.context import Context
from compilation.ast.auxiliary import NodeE


def normaliza(typevar):
    if typevar == VariableType.INT or typevar == MethodType.INT:
        return "int"
    if typevar == VariableType.BOOL or typevar == MethodType.BOOL:
        return "bool"
    if typevar == VariableType.DOUBLE or typevar == MethodType.DOUBLE:
        return "double"
    if typevar == VariableType.STRING or typevar == MethodType.STRING:
        return "str"
    if typevar == MethodType.VOID:
        return "void"


class Program(Node):
    def __init__(self):
        self.isfuncion = False
        self.statements = []
        self.padre = None
        self.listaDReturns = []

    def validate(self, context: Context):
        for dec in self.statements:
            if not dec.validate(context):
                return False
        return True

    def checktype(self, context: Context):
        countReturn = 0
        for statement in self.statements:
            if isinstance(statement, ReturnNode):
                countReturn += 1
            if not statement.checktype(context):
                return False
        return True

    @staticmethod
    def type() -> str:
        return "Program"


class Expression(Node):
    def __init__(self):
        self.nododreconocimiento = NodeE()
        self.noderaiz = NodeE()

    def checktype(self, context: Context):
        return self.noderaiz.checktype(context)

    def validate(self, context: Context):
        if not self.noderaiz.validate(context):
            return False
        return True


class Condition(Node):
    def __init__(self):
        self.expression1 = Expression()
        self.expression2 = Expression()
        self.comparador = None

    def validate(self, context: Context):
        return self.expression1.validate(context) and self.expression2.validate(context)

    def checktype(self, context: Context):
        if self.expression2.nododreconocimiento.ast is None:
            if self.expression1.checktype(context) != "bool":
                return False
            else:
                return True

        elif self.expression1.checktype(context) == self.expression2.checktype(context):
            return True
        else:
            return False

    @staticmethod
    def type() -> str:
        return "Conditional"


class Val(Node):
    def __init__(self, val):
        self.val = val

    def validate(self, context: Context):
        return True

    def checktype(self, context: Context):
        if self.val.token_type == TokenType.T_I_VALUE:
            return "int"
        if self.val.token_type == TokenType.T_DOUBLE:
            return "double"
        if self.val.token_type == TokenType.T_FALSE or TokenType.T_TRUE:
            return "bool"
        if self.val.token_type == TokenType.T_S_VALUE:
            return "str"

    @staticmethod
    def type() -> str:
        return "EXP"


class Variable(Node):
    padre = None

    def __init__(self, token: Token):
        self.idvar = token.value

    def validate(self, context: Context):
        return context.check_var(self.idvar)

    def checktype(self, context: Context):
        type = context.gettypevar(self.idvar)
        if type == VariableType.INT:
            return "int"
        if type == VariableType.BOOL:
            return "bool"
        if type == VariableType.DOUBLE:
            return "double"
        if type == VariableType.STRING:
            return "str"

    @staticmethod
    def type() -> str:
        return "Variable"


class FunCall(Node):
    def __init__(self):
        self.id = ""
        self.args = []

    def validate(self, context: Context) -> bool:
        for expr in self.args:
            if not expr.validate(context):
                return False
        return context.check_fun(self.id, len(self.args))

    def checktype(self, context: Context):
        type = context.gettypefun(self.id)
        if type == MethodType.INT:
            return "int"
        if type == MethodType.BOOL:
            return "bool"
        if type == MethodType.DOUBLE:
            return "double"
        if type == MethodType.STRING:
            return "str"

    @staticmethod
    def type() -> str:
        return "FunCall"


class Statement(Node):
    def __repr__(self) -> str:
        return "STATEMENT"


class D_Assign(Statement):
    def __init__(self):
        self.typevar = None
        self.id = ""
        self.expr = None
        self.isarray = False
        self.arrayvalue = []

    def validate(self, context: Context) -> bool:
        if not self.isarray:
            if not self.expr.validate(context):
                return False
            if not context.define_var(self.id, self.typevar,self.token):
                return False
        else:
            for expresion in self.arrayvalue:
                if not expresion.validate(context):
                    return False
        return True

    def checktype(self, context: Context):
        if not self.isarray:
            typeExpression = self.expr.checktype(context)
            type = normaliza(self.typevar)
            if typeExpression == type:
                return True
            return False
        else:
            for expression in self.arrayvalue:
                typeExpression = expression.checktype(context)
                if typeExpression != self.typevar:
                    return False
            return True

    @staticmethod
    def type() -> str:
        return "DecAssign"


class ReturnNode(Statement):
    def __init__(self):
        self.type = ""
        self.expr = Expression()
        self.padre = None

    def validate(self, context: Context):
        if not self.expr.validate(context):
            return False
        return True

    def checktype(self, context: Context):
        if normaliza(self.padre.padre.typefun) == self.expr.checktype(context):
            return True
        return False


class Redefinition(Statement):
    def __init__(self):
        self.id = None
        self.op = None
        self.expr = None

    def validate(self, context: Context) -> bool:
        if not self.expr.validate(context):
            return False

        if not context.check_var(self.id):
            return False

        return True

    def checktype(self, context: Context):
        return self.op.checktype(context)

    @staticmethod
    def type() -> str:
        return "Redef"


class Def_Fun(Statement):
    def __init__(self):
        self.typefun: MethodType
        self.idfun: str
        self.args = []
        self.body: Program
        self.nuevocontext: Context

    def validate(self, context: Context) -> bool:
        self.nuevocontext = context.crearnuevocontexto()
        for arg in self.args:
            if not self.nuevocontext.define_var(arg[1], arg[0],self.token):
                return False
        if not self.body.validate(self.nuevocontext):
            return False
        context.define_fun(self.idfun, self.typefun, self.args)

    def checktype(self, context: Context):
        return self.body.checktype(self.nuevocontext)

    @staticmethod
    def type() -> str:
        return "DefFun"


class IfCond(Statement):
    def __init__(self):
        self.operadoresbinarios = []
        self.conditions = []
        self.body = Program()
        self.nodoelse = None
        self.nuevocontexto: Context

    def validate(self, context: Context):
        for condition in self.conditions:
            if not condition.validate(context):
                return False
        if not self.body.validate(context):
            return False
        if self.nodoelse is not None:
            if not self.nodoelse.validate(context):
                return False
        return True

    def checktype(self, context: Context):
        for condition in self.conditions:
            if not condition.checktype(context):
                return False
        if not self.body.checktype(context):
            return False
        if self.nodoelse is not None:
            if not self.nodoelse.checktype(context):
                return False
        return True

    @staticmethod
    def type() -> str:
        return "If"


class WhileCond(Statement):
    def __init__(self):
        self.operadoresbinarios = []
        self.conditions = []
        self.body = Program()
        self.nuevocontexto = None

    def validate(self, context: Context):
        for condition in self.conditions:
            if not condition.validate(context):
                return False
        self.nuevocontexto = context.crearnuevocontexto()
        if not self.body.validate(self.nuevocontexto):
            return False
        return True

    def checktype(self, context: Context):
        for condition in self.conditions:
            if not condition.checktype(context):
                return False

        if not self.body.checktype(self.nuevocontexto):
            return False
        return True

    @staticmethod
    def type() -> str:
        return "While"
