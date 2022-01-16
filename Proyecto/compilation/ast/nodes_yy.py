from compilation.ast.nodes import Node


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


class Expression(Node):
    def __init__(self):
        self.nododreconocimiento = NodeE()
        self.noderaiz = NodeE()
        self.noderaiz = self.nododreconocimiento

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
        self.comparador: Rel = None

    def validate(self, context: Context):
        return self.expression1.validate(context) and self.expression2.validate(context)

    def checktype(self, context: Context):
        if self.expression2.nododreconocimiento.ast == None:
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


class NodeB(Node):
    def __init__(self):
        self.padre = None
        self.hijos = list()
        self.ast = None

    def refreshAST(self):
        if len(self.hijos) == 2:
            self.ast = self.hijos[1].ast


class NodeX(Node):
    def __init__(self):
        self.padre = None
        self.hijos = list()
        self.ast = None

    def refreshAST(self):
        if len(self.hijos) == 3:
            if isinstance(self.hijos[0], NodeAdd):
                if isinstance(self.padre, NodeX):
                    self.ast: Node = AddOp(self.padre.hijos[1].ast, self.hijos[2].ast)
                else:
                    self.ast: Node = AddOp(self.padre.hijos[0].ast, self.hijos[2].ast)
            elif isinstance(self.hijos[0], NodeSub):
                if isinstance(self.padre, NodeX):
                    self.ast: Node = SubOp(self.padre.hijos[1].ast, self.hijos[2].ast)
                else:
                    self.ast: Node = SubOp(self.padre.hijos[0].ast, self.hijos[2].ast)

        elif len(self.hijos) == 0:
            if isinstance(self.padre, NodeX):
                self.ast: Node = self.padre.hijos[1].ast
            else:
                self.ast: Node = self.padre.hijos[0].ast


class NodeM(Node):
    def __init__(self, *args, **kwargs):
        self.padre = None
        self.hijos = list()
        self.ast = None

    def refreshAST(self):
        if len(self.hijos) == 3:
            self.ast = self.hijos[1].ast
        elif len(self.hijos) == 1:
            self.ast = self.hijos[0].ast
        else:
            self.ast = None


class NodeY:
    def __init__(self):
        self.ast = None
        self.padre = None
        self.hijos = list()

    def refreshAST(self):
        if len(self.hijos) == 3:
            if isinstance(self.hijos[0], NodeMult):
                if isinstance(self.padre, NodeY):
                    self.ast: Node = MulOp(self.padre.hijos[1].ast, self.hijos[2].ast)
                else:
                    self.ast: Node = MulOp(self.padre.hijos[0].ast, self.hijos[2].ast)
            elif isinstance(self.hijos[0], NodeDiv):
                if isinstance(self.padre, NodeY):
                    self.ast: Node = DivOp(self.padre.hijos[1].ast, self.hijos[2].ast)
                else:
                    self.ast: Node = DivOp(self.padre.hijos[0].ast, self.hijos[2].ast)
            elif isinstance(self.hijos[0], NodeMod):
                if isinstance(self.padre, NodeY):
                    self.ast: Node = ModOp(self.padre.hijos[1].ast, self.hijos[2].ast)
                else:
                    self.ast: Node = ModOp(self.padre.hijos[0].ast, self.hijos[2].ast)
            elif isinstance(self.hijos[0], NodeExp):
                if isinstance(self.padre, NodeY):
                    self.ast: Node = ExpOp(self.padre.hijos[1].ast, self.hijos[2].ast)
                else:
                    self.ast: Node = ExpOp(self.padre.hijos[0].ast, self.hijos[2].ast)

        elif len(self.hijos) == 0:
            if isinstance(self.padre, NodeY):
                self.ast = self.padre.hijos[1].ast
            else:
                self.ast = self.padre.hijos[0].ast

    def __init__(self):
        self.ast = None
        self.padre = None
        self.hijos = list()

    def refreshAST(self):
        if len(self.hijos) == 3:
            if isinstance(self.hijos[0], NodeMult):
                if isinstance(self.padre, NodeY):
                    self.ast: Node = MulOp(self.padre.hijos[1].ast, self.hijos[2].ast)
                else:
                    self.ast: Node = MulOp(self.padre.hijos[0].ast, self.hijos[2].ast)
            elif isinstance(self.hijos[0], NodeDiv):
                if isinstance(self.padre, NodeY):
                    self.ast: Node = DivOp(self.padre.hijos[1].ast, self.hijos[2].ast)
                else:
                    self.ast: Node = DivOp(self.padre.hijos[0].ast, self.hijos[2].ast)
            elif isinstance(self.hijos[0], NodeMod):
                if isinstance(self.padre, NodeY):
                    self.ast: Node = ModOp(self.padre.hijos[1].ast, self.hijos[2].ast)
                else:
                    self.ast: Node = ModOp(self.padre.hijos[0].ast, self.hijos[2].ast)
            elif isinstance(self.hijos[0], NodeExp):
                if isinstance(self.padre, NodeY):
                    self.ast: Node = ExpOp(self.padre.hijos[1].ast, self.hijos[2].ast)
                else:
                    self.ast: Node = ExpOp(self.padre.hijos[0].ast, self.hijos[2].ast)

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
    padre = None

    @staticmethod
    def type() -> str:
        return "EXP"


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
