from compilation.errors import IncorrectCallError
from compilation.tokens import Token


class Context:
    def __init__(self):
        self.variables = {}
        self.funciones = {}
        self.errors = []
        self.contextPadre = None
        self.enfuncion = None
        self.enwhile = None

    def evalAttribute(self, idvar):
        evalexpr = self.variables[idvar].expr.noderaiz.eval(self)
        if not isinstance(evalexpr, RuntimeError):
            self.variables[idvar].value = evalexpr
        else:
            return evalexpr

    def getFunction(self, id):
        funContain = self.funciones.get(id, "NoEsta")
        if funContain != "NoEsta":
            return funContain
        else:
            context = self.contextPadre
            while context is not None:
                funContain = context.funciones.get(id, "NoEsta")
                if funContain != "NoEsta":
                    return funContain
                context = context.contextPadre

    def getvalueAttribute(self, var, token):
        if self.variables.get(var, "NoEsta") != "NoEsta":
            if self.variables[var].value is not None:
                return self.variables[var].value
            else:
                return RuntimeError("local variable {} referenced before assignment".format(var), "", token.line,
                                    token.column)
        else:
            context = self.contextPadre
            while context is not None:
                if context.variables.get(var, "NoEsta") != "NoEsta":
                    retorno = context.variables[var].value
                    if retorno is not None:
                        return retorno
                    else:
                        return RuntimeError("local variable {} referenced before assignment".format(var), "",
                                            token.line, token.column)
                context = context.padre

    def gettypefun(self, idfun):
        Esta = self.funciones.get(idfun, "NoEsta")
        if Esta != "NoEsta":
            return self.funciones[idfun].typefun
        else:
            context = self.contextPadre
            while context is not None:
                funContain = context.funciones.get(idfun, "NoEsta")
                if funContain != "NoEsta":
                    return context.funciones[idfun].typefun
                context = context.contextPadre

    def gettypevar(self, idvar: str):
        Esta = self.variables.get(idvar, "NoEsta")
        if Esta != "NoEsta":
            return self.variables[idvar].typevar
        else:
            context = self.contextPadre
            while context is not None:
                varContain = context.variables.get(idvar, "NoEsta")
                if varContain != "NoEsta":
                    return context.variables[idvar].typevar
                context = context.contextPadre

    def check_var(self, var: str, token: Token):
        varContain = self.variables.get(var, "NoEsta")
        if varContain != "NoEsta":
            return True
        else:
            context = self.contextPadre
            while context is not None:
                varContain = context.variables.get(var, "NoEsta")
                if varContain != "NoEsta":
                    return True
                context = context.contextPadre
            return IncorrectCallError("there is no variable with this name accessible from this scope", "", token.line,
                                      token.column)

    def check_fun(self, fun: str, args: int, token: Token):
        funContain = self.funciones.get(fun, "NoEsta")
        if funContain != "NoEsta":
            if args == len(funContain.args):
                return True
            else:
                return IncorrectCallError("the number of parameters entered into the function is not correct", "",
                                          token.line, token.column)
        else:
            context = self.contextPadre
            while context is not None:
                funContain = context.funciones.get(fun, "NoEsta")
                if funContain != "NoEsta":
                    if args == len(funContain.args):
                        return True
                    else:
                        return IncorrectCallError("the number of parameters entered into the function is not correct",
                                                  "", token.line, token.column)
                context = context.contextPadre
            return IncorrectCallError("there is no function with this name accessible from this scope", "", token.line,
                                      token.column)

    def define_fun(self, fun: str, node, token: Token):
        funContain = self.funciones.get(fun, "NoEsta")
        if funContain != "NoEsta":
            return IncorrectCallError("a function with this name already exists in this context", "", token.line,
                                      token.column)
        else:
            self.funciones.setdefault(fun, node)
        return True

    def define_var(self, id: str, var, token: Token):
        varContain = self.variables.get(id, "NoEsta")
        if varContain != "NoEsta":
            return IncorrectCallError("a variable with this name already exists in this context", "", token.line,
                                      token.column)
        else:
            self.variables.setdefault(id, var)
        return True

    def crearnuevocontexto(self):
        nuevocontext = Context()
        nuevocontext.contextPadre = self
        return nuevocontext
