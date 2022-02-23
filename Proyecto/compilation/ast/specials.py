from compilation.ast.nodes import Statement, normaliza
from compilation.context import Context
from compilation.errors import CheckTypesError
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
        return CheckTypesError("The induced type of the expression is different from the type of the variable", "",
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
        self.varsforEnvironment = [[]]
        self.functionsOfBikes = []
        self.token = None
        self.body = None

    def validate(self, context: Context):
        self.nuevocontext = context.crearnuevocontexto()
        self.addvars()

        validationbody = self.body.validate(self.nuevocontext)
        if not isinstance(validationbody, bool):
            return validationbody
        return True

    def checktype(self, context: Context):
        return self.body.checktype(self.nuevocontext)

    def eval(self, context: Context):
        return self.body.eval(self.nuevocontext)

    def addvars(self):
        listvar = []
        if isinstance(self, RiderNode):
            listvar = self.varsforRiders
        elif isinstance(self, BikeNode):
            listvar = self.varsforBikes
        elif isinstance(self, EnvironmentNode):
            listvar = self.varsforEnvironment

        for var in listvar:
            assign = D_Assign()
            assign.id = var[0]
            assign.value = var[2]
            assign.typevar = var[1]
            self.nuevocontext.define_var(var[0], assign, self.token)
        if not isinstance(self, EnvironmentNode) and isinstance(self, RiderNode):
            listvarsofenviroment = self.varsforEnvironment
            for var in listvarsofenviroment:
                assign = D_Assign()
                assign.id = var[0]
                assign.value = var[2]
                assign.typevar = var[1]
                self.nuevocontext.define_var(var[0], assign, self.token)


class BikeNode(TypeSpecial):
    def __init__(self):
        super().__init__()

        self.varsforBikes = [["brand", VariableType.STRING, "Ducati"], ["max_speed", VariableType.DOUBLE, 362.4],
                             ["weight", VariableType.INT, 157], ["tires", VariableType.INT, 3],
                             ["brakes", VariableType.INT, 5], ["chassis_stiffness", VariableType.INT, 8],
                             ["model", VariableType.STRING, "RS-GP 2021"]]
        self.functionsOfBikes = ["select_configuration"]

    def refreshContext(self, dict_bike, dict_weather):
        keys_dict_bike = list(dict_bike.keys())
        for key in keys_dict_bike:
            if list(self.nuevocontext.variables.keys()).count(key) == 1:
                self.nuevocontext.variables[key].value = dict_bike[key]

        keys_dict_weather = list(dict_weather.keys())
        for key in keys_dict_weather:
            if list(self.nuevocontext.variables.keys()).count(key) == 1:
                self.nuevocontext.variables[key].value = dict_weather[key]


class RiderNode(TypeSpecial):
    def __init__(self):
        super().__init__()

        self.varsforEnvironment = [["weather_status", VariableType.INT, 0], ["wind", VariableType.INT, 5],
                                   ["temperature", VariableType.INT, 5], ["visibility", VariableType.INT, 5],
                                   ["humidity", VariableType.INT, 5], ["wind_intensity", VariableType.INT, 5]]

        self.varsforRiders = [["speed", VariableType.DOUBLE, 0.0], ["acceleration", VariableType.DOUBLE, 0.0],
                              ["time_lap", VariableType.DOUBLE, 0.0], ["cornering", VariableType.INT, 5],
                              ["step_by_line", VariableType.INT, 5],
                              ["probability_of_falling_off_the_bike", VariableType.INT, 5],
                              ["independence", VariableType.INT, 5], ["expertise", VariableType.INT, 5],
                              ["aggressiveness", VariableType.INT, 5], ["length", VariableType.DOUBLE, 0.0],
                              ["max_speed", VariableType.DOUBLE, 0.0], ["orientation", VariableType.INT, 0],
                              ["type", VariableType.INT, 0], ["pit_line", VariableType.INT, 0],
                              ["pit_length", VariableType.DOUBLE, 0.0]]

        self.functionsOfRiders = ["select_acceleration", "select_action"]

    def refreshContext(self, dict_agent, dict_rider, dict_section, dict_weather):

        keys_dict_agent = list(dict_agent.keys())
        for key in keys_dict_agent:
            if list(self.nuevocontext.variables.keys()).count(key) == 1:
                self.nuevocontext.variables[key].value = dict_agent[key]

        keys_dict_rider = list(dict_rider.keys())
        for key in keys_dict_rider:
            if list(self.nuevocontext.variables.keys()).count(key) == 1:
                self.nuevocontext.variables[key].value = dict_rider[key]

        keys_dict_section = list(dict_section.keys())
        for key in keys_dict_section:
            if list(self.nuevocontext.variables.keys()).count(key) == 1:
                self.nuevocontext.variables[key].value = dict_section[key]

        keys_dict_weather = list(dict_weather.keys())
        for key in keys_dict_weather:
            if list(self.nuevocontext.variables.keys()).count(key) == 1:
                self.nuevocontext.variables[key].value = dict_weather[key]


class EnvironmentNode(TypeSpecial):
    def __init__(self):
        super().__init__()
        self.varsforEnvironment = [["track", VariableType.STRING, "Misano"], ["weather_status", VariableType.INT, 0],
                                   ["wind", VariableType.INT, 5], ["temperature", VariableType.INT, 5],
                                   ["visibility", VariableType.INT, 5], ["humidity", VariableType.INT, 5],
                                   ["wind_intensity", VariableType.INT, 5]]

    def refreshContext(self, dict_weather):

        keys_dict_weather = list(dict_weather.keys())
        for key in keys_dict_weather:
            if list(self.nuevocontext.variables.keys()).count(key) == 1:
                self.nuevocontext.variables[key].value = dict_weather[key]
