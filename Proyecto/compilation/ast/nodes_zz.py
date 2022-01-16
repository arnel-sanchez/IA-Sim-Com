from compilation.ast.nodes import Node


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
            if not context.define_var(self.id, self.typevar):
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
            for expression in arrayvalue:
                typeExpression = expression.checktype(context)
                if typeExpression != typevar:
                    return False
            return True

    @staticmethod
    def type() -> str:
        return "DecAssign"


class ReturnNode(Statement):
    type = ""
    expr: Expression = Expression()
    padre = None

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
        self.expr: Expression = None

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
    typefun: MethodType
    idfun: str
    args: list(list()) = []
    body: Program
    nuevocontext: Context = None

    def validate(self, context: Context) -> bool:
        self.nuevocontext = context.crearnuevocontexto()

        for arg in self.args:
            if not self.nuevocontext.define_var(arg[1], arg[0]):
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
        self.conditions: list(Condition) = []
        self.body = Program()
        self.nodoelse = None
        self.nuevocontexto: Context = None

    def validate(self, context: Context):

        for condition in self.conditions:
            if not condition.validate(context):
                return False

        if not self.body.validate(context):
            return False

        if self.nodoelse != None:
            if not self.nodoelse.validate(context):
                return False
        return True

    def checktype(self, context: Context):
        for condition in self.conditions:
            if not condition.checktype(context):
                return False

        if not self.body.checktype(context):
            return False

        if self.nodoelse != None:
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
