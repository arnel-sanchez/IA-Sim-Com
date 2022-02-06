from compilation.ast.nodes import Node, normaliza, Statement
from compilation.context import Context
from compilation.ast.specials import RiderNode, BikeNode
from compilation.errors import IncorrectCallError, CheckTypesError
from compilation.ast.auxiliary import NodeE


def verificatealwaysReturn(dec):
    for statement in dec.body.statements:
        if isinstance(statement, ReturnNode):
            if dec.nodoelse is None:
                if isinstance(dec, Program):
                    return True
                else:
                    return False
            elif isinstance(dec.nodoelse, IfCond):
                if verificatealwaysReturn(dec.nodoelse):
                    return True
            elif isinstance(dec.nodoelse, Program):
                for statementdprogram in dec.nodoelse.statements:
                    if isinstance(statementdprogram, ReturnNode):
                        return True
                    elif isinstance(statementdprogram, IfCond):
                        if verificatealwaysReturn(statementdprogram):
                            return True
        elif isinstance(statement, IfCond):
            if verificatealwaysReturn(statement):
                return True
    return False


class Program(Node):
    def __init__(self):
        self.isfuncion: bool = False
        self.statements = []
        self.padre = None
        self.listaDReturns = []
        self.token = None

    def validate(self, context: Context):
        if isinstance(self.padre, WhileCond):
            for statement in self.statements:
                if isinstance(statement, Def_Fun):
                    return False  # Error ,No puede definir una funcion dentro de un while
                elif isinstance(statement, RiderNode) or isinstance(statement, BikeNode):
                    return False  # Error ,No puede definir un tipo especial dentro de un while
                    # if isinstance(statement,Redefinition) or isinstance(statement,D_Assign) or isinstance(statement,WhileCond) or isinstance(statement,IfCond) or isinstance(statement,FunCall):  #estas son las declaraciones que pueden estar en cualquier ambito
                validationstatement = statement.validate(context)
                if not isinstance(validationstatement, bool):
                    return validationstatement
        elif isinstance(self.padre, IfCond):
            for statement in self.statements:
                if isinstance(statement, Def_Fun):
                    return False  # Error ,No puede definir una funcion dentro de un If
                elif isinstance(statement, RiderNode) or isinstance(statement, BikeNode):
                    return False  # Error ,No puede definir un tipo especial dentro de un if
                elif isinstance(statement, ReturnNode) and (statement.type == "continue" or statement.type == "break"):
                    if context.enwhile is None:
                        return IncorrectCallError("This token is incorrect, it is not within a while scope", "",
                                                  self.token.line, self.token.column)
                    # Error ,Esta declaracion no es valida dentro de un If
                    # if isinstance(statement,Redefinition) or isinstance(statement,D_Assign) or isinstance(statement,WhileCond) or isinstance(statement,IfCond) or isinstance(statement,FunCall):  #estas son las declaraciones que pueden estar en cualquier ambito
                validationstatement = statement.validate(context)
                if not isinstance(validationstatement, bool):
                    return validationstatement
        elif isinstance(self.padre, Def_Fun):
            listIF = []
            aseguraretorno = False
            for statement in self.statements:
                if isinstance(statement, Def_Fun):
                    return False  # Error ,No puede definir una funcion dentro de una funcion
                elif isinstance(statement, RiderNode) or isinstance(statement, BikeNode):
                    return False  # Error ,No puede definir un tipo especial dentro de una funcion
                elif isinstance(statement, ReturnNode) and (statement.type == "continue" or statement.type == "break"):
                    return False  # Error ,Esta declaracion no es valida dentro de una funcion
                else:
                    if isinstance(statement, ReturnNode):
                        validationstatement = statement.validate(context)
                        if not isinstance(validationstatement, bool):
                            return validationstatement
                        else:
                            aseguraretorno = True
                    else:

                        if isinstance(statement, IfCond):
                            listIF.append(statement)
                        validationstatement = statement.validate(context)
                        if not isinstance(validationstatement, bool):
                            return validationstatement
            for dec_if in listIF:
                if verificatealwaysReturn(dec_if):
                    aseguraretorno = True
            if normaliza(self.padre.typefun) != "void":
                if aseguraretorno:
                    return aseguraretorno  # No se asegura que se retorne  , Error
                else:
                    return IncorrectCallError(" Not all code paths return a value	", "", self.token.line,
                                              self.token.column)
        else:
            if self.padre is None:
                for statement in self.statements:

                    if isinstance(statement, ReturnNode):
                        return False  # Error ,Esta declaracion no es valida
                    validationstatement = statement.validate(context)
                    if not isinstance(validationstatement, bool):
                        return validationstatement
            else:
                for statement in self.statements:
                    if isinstance(statement, Def_Fun):
                        return False  # Error ,No puede definir una funcion en este ambito
                    elif isinstance(statement, RiderNode) or isinstance(statement, BikeNode):
                        return False  # Error ,No puede definir un tipo especial en este ambito
                    elif isinstance(statement, ReturnNode):
                        if (statement.type == "continue" or statement.type == "break") and context.enwhile is None:
                            return IncorrectCallError("This token is incorrect, it is not within a while scope", "",
                                                      self.token.line, self.token.column)

                    validationstatement = statement.validate(context)
                    if not isinstance(validationstatement, bool):
                        return validationstatement
        return True

    def checktype(self, context: Context):
        for statement in self.statements:
            checktypeStatement = statement.checktype(context)
            if isinstance(checktypeStatement, CheckTypesError):
                return checktypeStatement
        return True

    def eval(self, context: Context):
        for statement in self.statements:
            if not isinstance(statement, Def_Fun):
                if not isinstance(statement, ReturnNode):
                    evaluation = statement.eval(context)
                    if isinstance(evaluation, RuntimeError):
                        return evaluation
                    if evaluation is not None:
                        if evaluation == "break" or evaluation == "continue":
                            return evaluation
                        elif evaluation != "Nothing":
                            return evaluation
                        else:
                            if isinstance(self.padre, Def_Fun):
                                return
                            else:
                                return "Nothing"
                elif statement.type == "break":
                    return "break"
                elif statement.type == "continue":
                    return "continue"
                else:
                    if statement.expr.noderaiz.ast is not None:
                        return statement.expr.eval(context)
                    else:
                        if isinstance(self.padre, Def_Fun):
                            return
                        else:
                            return "Nothing"

    @staticmethod
    def type() -> str:
        return "Program"


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


class D_Assign(Statement):
    def __init__(self):
        self.typevar = None
        self.id = None
        self.expr = None
        self.isarray: bool = False
        self.arrayvalue = []
        self.token = None
        self.value = None

    def validate(self, context: Context) -> bool:  # @@
        if not self.isarray:
            validationexpr = self.expr.validate(context)
            if not isinstance(validationexpr, bool):
                validationexpr.line = self.token.line
                validationexpr.column = self.token.column
                return validationexpr
            validationvar = context.define_var(self.id, self, self.token)
            if not isinstance(validationvar, bool):
                return validationvar
        else:
            for expresion in self.arrayvalue:
                if not expresion.validate(context):
                    return False
        return True

    def checktype(self, context: Context):
        if not self.isarray:
            typeExpression = self.expr.checktype(context)
            type = normaliza(self.typevar)
            if isinstance(typeExpression, CheckTypesError):
                typeExpression.line = self.token.line
                typeExpression.column = self.token.column
                return typeExpression
            if typeExpression == type:
                return True
            return CheckTypesError("the induced type of the expression is different from the type of the variable", "",
                                   self.token.line, self.token.column)
        else:
            for expression in arrayvalue:
                typeExpression = expression.checktype(context)
                if typeExpression != typevar:
                    return False
            return True

    def eval(self, context: Context):
        return context.evalAttribute(self.id)

    @staticmethod
    def type() -> str:
        return "DecAssign"


class ReturnNode(Statement):
    def __init__(self):
        self.type = ""
        self.expr: Expression = Expression()
        self.padre = None
        self.token = None

    def validate(self, context: Context):

        if self.type == "continue" or self.type == "break":
            return True

        if context.enfuncion is None:
            return IncorrectCallError("You can not return pq is not within the scope of a function", "",
                                      self.token.line, self.token.column)

        elif normaliza(context.enfuncion.typefun) == "void":
            if self.expr.noderaiz.ast is not None:
                return IncorrectCallError("The function does not expect to return an expression", "", self.token.line,
                                          self.token.column)

        else:
            if self.expr.noderaiz.ast is None:
                return IncorrectCallError("An expression must be returned to the function", "", self.token.line,
                                          self.token.column)

            validationexpr = self.expr.validate(context)
            if not isinstance(validationexpr, bool):
                validationexpr.line = self.token.line
                validationexpr.column = self.token.column
                return validationexpr

        return True

    def checktype(self, context: Context):
        if self.type == "continue" or self.type == "break":
            return True

        elif normaliza(context.enfuncion.typefun) != "void":
            checkexpr = self.expr.checktype(context)
            if isinstance(checkexpr, CheckTypesError):
                checkexpr.line = self.token.line
                checkexpr.column = self.token.column
                return checkexpr
            if normaliza(context.enfuncion.typefun) == checkexpr:
                return True
            else:
                return CheckTypesError(
                    "the type of the expression does not correspond to the type that the method should return", "",
                    self.token.line, self.token.column)

        return True


class Redefinition(Statement):
    def __init__(self):
        self.id = None
        self.op = None
        self.expr = None
        self.token = None

    def validate(self, context: Context) -> bool:
        validationexpr = self.expr.validate(context)
        if not isinstance(validationexpr, bool):
            validationexpr.line = self.token.line
            validationexpr.column = self.token.column
            return validationexpr

        return context.check_var(self.id, self.token)

    def checktype(self, context: Context):
        return self.op.checktype(context)

    def eval(self, context: Context):
        evaloper = self.op.eval(context)
        if isinstance(evaloper, RuntimeError):
            return evaloper
        context.variables[self.id].value = evaloper

    @staticmethod
    def type() -> str:
        return "Redef"


class Def_Fun(Statement):
    def __init__(self):
        self.padre = None
        self.typefun = None
        self.idfun = None
        self.args = []
        self.body = None
        self.nuevocontext = None
        self.token = None

    def validate(self, context: Context) -> bool:
        if not isinstance(self.padre, RiderNode) and not isinstance(self.padre, BikeNode):
            self.nuevocontext = context.crearnuevocontexto()
        else:
            self.nuevocontext = context

        validationfun = context.define_fun(self.idfun, self, self.token)
        if not isinstance(validationfun, bool):
            return validationfun

        for arg in self.args:
            var = D_Assign()
            var.typevar = arg[0]
            var.token = self.token
            validationArgs = self.nuevocontext.define_var(arg[1], var, self.token)
            if not isinstance(validationArgs, bool):
                return validationArgs

        self.nuevocontext.enfuncion = self
        validationbody = self.body.validate(self.nuevocontext)
        if not isinstance(validationbody, bool):
            return validationbody

        return True

    def checktype(self, context: Context):
        return self.body.checktype(self.nuevocontext)

    def eval(self, args, context: Context):
        keys = list(self.nuevocontext.variables.keys())
        index = 0
        for arg in args:
            evalexpression = arg.eval(context)
            if not isinstance(evalexpression, RuntimeError):
                self.nuevocontext.variables[keys[index]].value = evalexpression
                index += 1
            else:
                return evalexpression
        return self.body.eval(self.nuevocontext)

    @staticmethod
    def type() -> str:
        return "DefFun"


class Condition(Node):
    def __init__(self):
        self.expression1 = Expression()
        self.expression2 = Expression()
        self.comparador = None
        self.token = None

    def validate(self, context: Context):
        validationExpr1 = self.expression1.validate(context)
        if isinstance(validationExpr1, IncorrectCallError):
            return validationExpr1
        if self.expression2.nododreconocimiento.ast is not None:
            validationExpr2 = self.expression2.validate(context)
            if isinstance(validationExpr2, IncorrectCallError):
                return validationExpr2
        return True

    def checktype(self, context: Context):
        checkExpr1 = self.expression1.checktype(context)
        if self.expression2.nododreconocimiento.ast is None:
            if isinstance(checkExpr1, CheckTypesError):
                return checkExpr1
            else:
                return True
        else:
            checktypecomp = self.comparador.checktype(context)
            if isinstance(checktypecomp, CheckTypesError):
                if checktypecomp.line == "":
                    checktypecomp.line = self.token.line
                    checktypecomp.column = self.token.column
                return checktypecomp
            else:
                return True
            # checkExpr2=self.expression2.checktype(context)
            # if isinstance(checkExpr2,CheckTypesError):
            # return checkExpr2
            # if checkExpr1==checkExpr2:
            #    return True
            # else:
            #  return IncorrectCallError("Cannot compare two expressions with different types","","","")

    def eval(self, context: Context):
        return self.comparador.eval(context)

    @staticmethod
    def type() -> str:
        return "Conditional"


class IfCond(Statement):
    def __init__(self):
        self.operadoresbinarios = []
        self.conditions = []
        self.body = Program()
        self.nodoelse = None

    def validate(self, context: Context):
        for condition in self.conditions:
            validationCondition = condition.validate(context)
            if not isinstance(validationCondition, bool):
                return validationCondition
        validationbody = self.body.validate(context)
        if not isinstance(validationbody, bool):
            return validationbody
        if self.nodoelse is not None:
            validationbodyelse = self.nodoelse.validate(context)
            if not isinstance(validationbodyelse, bool):
                return validationbodyelse
        return True

    def checktype(self, context: Context):
        for condition in self.conditions:
            checktypeCondition = condition.checktype(context)
            if isinstance(checktypeCondition, CheckTypesError):
                return checktypeCondition
        checktypeBody = self.body.checktype(context)
        if isinstance(checktypeBody, CheckTypesError):
            return checktypeBody
        if self.nodoelse is not None:
            checktypeNodoelse = self.nodoelse.checktype(context)
            if isinstance(checktypeNodoelse, CheckTypesError):
                return checktypeNodoelse

        return True

    def eval(self, context: Context):
        resultante = self.conditions[0].eval(context)
        if isinstance(resultante, RuntimeError):
            return resultante
        index = 1
        while index < len(self.conditions):
            self.operadoresbinarios[index - 1].left_node = resultante
            evalcond = self.conditions[index].eval(context)
            if isinstance(evalcond, RuntimeError):
                return evalcond
            self.operadoresbinarios[index - 1].right_node = evalcond
            resultante = self.operadoresbinarios[index - 1].eval(context)
            index += 1
        if resultante:
            return self.body.eval(context)
        elif self.nodoelse is not None:
            return self.nodoelse.eval(context)

    @staticmethod
    def type() -> str:
        return "If"


class WhileCond(Statement):
    def __init__(self):
        self.operadoresbinarios = []
        self.conditions = []
        self.body = Program()

    def validate(self, context: Context):
        for condition in self.conditions:
            validationcondition = condition.validate(context)
            if not isinstance(validationcondition, bool):
                return validationcondition
        context.enwhile = self
        validationbody = self.body.validate(context)
        if not isinstance(validationbody, bool):
            return validationbody
        context.enwhile = None
        return True

    def checktype(self, context: Context):
        for condition in self.conditions:
            checktypeCondition = condition.checktype(context)
            if isinstance(checktypeCondition, CheckTypesError):
                return checktypeCondition
        checktypeBody = self.body.checktype(context)
        if isinstance(checktypeBody, CheckTypesError):
            return checktypeBody
        return True

    def eval(self, context: Context):
        resultante = self.conditions[0].eval(context)
        if isinstance(resultante, RuntimeError):
            return resultante
        index = 1
        while index < len(self.conditions):
            self.operadoresbinarios[index - 1].left_node = resultante
            evalexpr = self.conditions[index].eval(context)
            if isinstance(evalexpr, RuntimeError):
                return evalexpr
            self.operadoresbinarios[index - 1].right_node = evalexpr
            resultante = self.operadoresbinarios[index - 1].eval(context)
            index += 1
        if resultante:
            retorno = self.body.eval(context)
            if retorno == "continue" or retorno is None:
                return self.eval(context)
            elif not isinstance(retorno, str):
                return retorno

    @staticmethod
    def type() -> str:
        return "While"
