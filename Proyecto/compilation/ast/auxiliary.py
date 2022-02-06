from compilation.ast.nodes import Node, normaliza
from compilation.context import Context
from compilation.tokens import TokenType
from compilation.tokens import Token
from compilation.enums import VariableType, MethodType
from compilation.errors import CheckTypesError


class NodeE(Node):
    def __init__(self):
        self.padre = None
        self.hijos = list()
        self.ast = None

    def refreshAST(self):
        if len(self.hijos) > 0:
            self.ast = self.hijos[1].ast

    def checktype(self, context: Context):
        return self.ast.checktype(context)

    def validate(self, context: Context):
        return self.ast.validate(context)

    def eval(self, context: Context):
        return self.ast.eval(context)


class NodeB(Node):
    def __init__(self):
        self.padre = None
        self.hijos = list()
        self.ast = None

    def refreshAST(self):
        if len(self.hijos) == 2:
            if isinstance(self.padre, NodeE):
                self.ast = self.hijos[1].ast
            else:
                self.ast = self.padre.hijos[0]
                self.ast.right_node = self.hijos[1].ast
                if isinstance(self.padre.padre, NodeE):
                    self.ast.left_node = self.padre.padre.hijos[0].ast
                else:
                    self.ast.left_node = self.padre.padre.hijos[1].ast


class NodeX(Node):
    def __init__(self):
        self.padre = None
        self.hijos = list()
        self.ast = None

    def refreshAST(self):
        if len(self.hijos) == 3:
            self.ast = self.hijos[2].ast

        elif len(self.hijos) == 0:
            if isinstance(self.padre, NodeX):
                self.ast: Node = self.padre.hijos[1].ast
            else:
                self.ast: Node = self.padre.hijos[0].ast


class NodeM(Node):
    def __init__(self):
        self.padre = None
        self.hijos = list()
        self.ast = None
        self.aux = None

    def refreshAST(self):
        if len(self.hijos) == 3:
            self.aux = self.hijos[1].ast
        elif len(self.hijos) == 1:
            self.aux = self.hijos[0].ast
        else:
            self.ast = None

        if self.aux is not None:
            if isinstance(self.padre, NodeB):
                self.ast = self.aux
            else:
                self.ast = self.padre.hijos[0]
                self.ast.right_node = self.aux
                if isinstance(self.padre.padre, NodeB):
                    self.ast.left_node = self.padre.padre.hijos[0].ast
                else:
                    self.ast.left_node = self.padre.padre.hijos[1].ast


class NodeY:
    def __init__(self):
        self.ast = None
        self.padre = None
        self.hijos = list()

    def refreshAST(self):
        if len(self.hijos) == 3:
            self.ast = self.hijos[2].ast

        elif len(self.hijos) == 0:
            if isinstance(self.padre, NodeY):
                self.ast = self.padre.hijos[1].ast
            else:
                self.ast = self.padre.hijos[0].ast


class NodeQ(Node):
    def __init__(self):
        self.padre = None
        self.hijos = list()
        self.ast = None

    def refreshAST(self):
        if len(self.hijos) == 1:
            self.ast = self.hijos[0]


class Nodepsilon(Node):
    def __init__(self):
        self.padre = None

    @staticmethod
    def type() -> str:
        return "EXP"


class Val(Node):  # @@
    def __init__(self, val):
        self.val = val
        self.type = None

    def validate(self, context: Context):
        return True

    def checktype(self, context: Context):
        if self.val.token_type == TokenType.T_I_VALUE:
            self.type = 9
            return "int"
        if self.val.token_type == TokenType.T_D_VALUE:
            self.type = 4.5
            return "double"
        if self.val.token_type == TokenType.T_FALSE or self.val.token_type == TokenType.T_TRUE:
            if self.val.token_type == TokenType.T_FALSE:
                self.type = False
            else:
                self.type = True
            return "bool"
        if self.val.token_type == TokenType.T_S_VALUE:
            self.type = "DD"
            return "str"

    def eval(self, context: Context):
        if self.type == True or self.type == False:
            return self.type
        else:
            return (type(self.type))(self.val.value)

    @staticmethod
    def type() -> str:
        return "EXP"


class Variable(Node):
    def __init__(self, token: Token):
        self.idvar = token.value
        self.token = token

    def validate(self, context: Context):
        return context.check_var(self.idvar, self.token)

    def checktype(self, context: Context):
        type_ = context.gettypevar(self.idvar)
        if type_ == VariableType.INT:
            return "int"
        if type_ == VariableType.BOOL:
            return "bool"
        if type_ == VariableType.DOUBLE:
            return "double"
        if type_ == VariableType.STRING:
            return "str"

    def eval(self, context: Context):
        return context.getvalueAttribute(self.idvar, self.token)

    @staticmethod
    def type() -> str:
        return "Variable"


class FunCall(Node):
    def __init__(self):
        self.id = None
        self.args = []
        self.token = None

    def validate(self, context: Context) -> bool:
        for expr in self.args:
            validationexpr = expr.validate(context)
            if not isinstance(validationexpr, bool):
                validationexpr.line = self.token.line
                validationexpr.column = self.token.column
                return validationexpr

        return context.check_fun(self.id, len(self.args), self.token)

    def checktype(self, context: Context):
        index = 0
        definitionfuncion = context.getFunction(self.id)
        keys = list(definitionfuncion.nuevocontext.variables.keys())
        for arg in self.args:
            typeExp = arg.checktype(context)
            if isinstance(typeExp, CheckTypesError):
                return typeExp
            if typeExp != normaliza(definitionfuncion.nuevocontext.variables[keys[index]].typevar):
                return CheckTypesError("the parameter entered is not of the expected type", "", self.token.line,
                                       self.token.column)  ##Anadir error (el parametro ingresado no es del tipo esperado)
            index += 1
        type_ = context.gettypefun(self.id)
        if type_ == MethodType.INT:
            return "int"
        if type_ == MethodType.BOOL:
            return "bool"
        if type_ == MethodType.DOUBLE:
            return "double"
        if type_ == MethodType.STRING:
            return "str"

    def eval(self, context: Context):
        return context.getFunction(self.id).eval(self.args, context)

    @staticmethod
    def type() -> str:
        return "FunCall"


class Expression(Node):
    def __init__(self):
        self.nododreconocimiento = NodeE()
        self.noderaiz = NodeE()
        self.noderaiz = self.nododreconocimiento

    def checktype(self, context: Context):
        return self.noderaiz.checktype(context)

    def validate(self, context: Context):
        return self.noderaiz.validate(context)

    def eval(self, context: Context):
        return self.noderaiz.eval(context)
