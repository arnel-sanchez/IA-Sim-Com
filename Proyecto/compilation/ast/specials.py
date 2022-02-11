from compilation.ast.nodes import Statement, normaliza
from compilation.context import Context
from compilation.ast.assignments import Assign
from compilation.errors import IncorrectCallError, CheckTypesError
from compilation.enums import VariableType


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
        typeExpression = self.expr.checktype(context)
        type_ = normaliza(self.typevar)
        if isinstance(typeExpression, CheckTypesError):
            typeExpression.line = self.token.line
            typeExpression.column = self.token.column
            return typeExpression
        if typeExpression == type_:
            return True
        return CheckTypesError("the induced type of the expression is different from the type of the variable", "",
                               self.token.line, self.token.column)

    def eval(self, context: Context):
        return context.evalAttribute(self.id)

    @staticmethod
    def type() -> str:
        return "DecAssign"


class TypeSpecial(Statement):
    def __init__(self):
        self.id = None
        self.padre = None
        self.funciones = []
        self.variables = []
        self.nuevocontext = None
        self.varsforRiders = [[]]
        self.functionsOfRiders = []
        self.varsforBikes = [[]]
        self.functionsOfBikes = []
        self.token = None

    def validate(self, context: Context):
        self.nuevocontext = context.crearnuevocontexto()
        self.addvars()
        if isinstance(self, RiderNode):
            for var in self.variables:
                if not isinstance(var.op, Assign):
                    return IncorrectCallError("in this context they can only be redefined with the equal operator", "",
                                              self.token.line, self.token.column)
                keys = list(self.nuevocontext.variables.keys())
                if keys.count(var.id) == 0 or (var.id != "cornering" and var.id != "step_by_line"):
                    return IncorrectCallError(
                        "only cornering variables and step_by_line belonging to the type can be redefined", "",
                        self.token.line, self.token.column)

                validationexpr = var.expr.validate(context)
                if not isinstance(validationexpr, bool):
                    validationexpr.line = self.token.line
                    validationexpr.column = self.token.column
                    return validationexpr
        else:
            if len(self.variables) > 0:
                return IncorrectCallError("within a bike type you can not redefine variables", "", self.token.line,
                                          self.token.column)
        # Hay que agregarle las variables de las motos o los pilotos
        for function in self.funciones:
            if isinstance(self, BikeNode):
                if self.functionsOfBikes.count(function.idfun) != 0:
                    self.functionsOfBikes.remove(function.idfun)
                else:
                    return IncorrectCallError(
                        "the method was already defined or it is not valid to define a method with this name in this context",
                        "", self.token.line, self.token.column)
            elif isinstance(self, RiderNode):
                if self.functionsOfRiders.count(function.idfun) != 0:
                    self.functionsOfRiders.remove(function.idfun)
                else:
                    return IncorrectCallError(
                        "the method was already defined or it is not valid to define a method with this name in this context",
                        "", self.token.line, self.token.column)
            if len(function.args) > 0:
                return IncorrectCallError("methods defined within a type must have no arguments", "", self.token.line,
                                          self.token.column)
            validationfun = function.validate(self.nuevocontext)
            if not isinstance(validationfun, bool):
                return validationfun
        return True

    def checktype(self, context: Context):
        for var in self.variables:
            checking = var.op.checktype(self.nuevocontext)
            if isinstance(checking, CheckTypesError):
                return checking
        for function in self.funciones:
            if ((function.idfun == "select_configuration" or function.idfun == "select_acceleration") and normaliza(
                    function.typefun) != "void") or (
                    function.idfun == "select_action" and normaliza(function.typefun) != "int"):
                return CheckTypesError("error in the return value of the function", "", self.token.line,
                                       self.token.column)
            checktypefunction = function.checktype(context)
            if isinstance(checktypefunction, CheckTypesError):
                return checktypefunction
        return True

    def eval(self, context: Context):
        for var in self.variables:
            evalvar = var.expr.eval(self.nuevocontext)
            if isinstance(evalvar, RuntimeError):
                return evalvar
            if evalvar > 10:
                return RuntimeError("this variable must be less than or equal to 10", "", self.token.line,
                                    self.token.column)
            if var.id == "cornering":
                self.varsforRiders[3][2] = evalvar
            else:
                self.varsforRiders[4][2] = evalvar
                # self.nuevocontext.variables[var.id].value=evalvar

    def addvars(self):
        if isinstance(self, RiderNode):
            listvar = self.varsforRiders
        else:
            listvar = self.varsforBikes
        for var in listvar:
            assign = D_Assign()
            assign.id = var[0]
            assign.value = var[2]
            assign.typevar = var[1]
            self.nuevocontext.define_var(var[0], assign, self.token)

    def refreshContext(self, dict_):
        keys = dict_.keys()
        for key in keys:
            if list(self.nuevocontext.variables.keys()).count(key) == 1:
                self.nuevocontext.variables[key].value = dict_[key]


class BikeNode(TypeSpecial):
    def __init__(self):
        super().__init__()

        self.varsforBikes = [["brand", VariableType.STRING, "Ducati"], ["max_speed", VariableType.DOUBLE, 362.4],
                             ["weight", VariableType.INT, 157], ["tires", VariableType.INT, 3],
                             ["brakes", VariableType.INT, 5], ["chassis_stiffness", VariableType.INT, 8]]
        self.functionsOfBikes = ["select_configuration"]


class RiderNode(TypeSpecial):
    def __init__(self):
        super().__init__()
        self.varsforRiders = [["speed", VariableType.DOUBLE, 0.0], ["acceleration", VariableType.DOUBLE, 0.0],
                              ["time_lap", VariableType.DOUBLE, 0.0], ["cornering", VariableType.INT, 5],
                              ["step_by_line", VariableType.INT, 5]]
        self.functionsOfRiders = ["select_acceleration", "select_action"]
