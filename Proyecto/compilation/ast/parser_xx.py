from compilation.tokens import TokenType, Token
from compilation.variables import VariableType, MethodType


def CreaNododProgram(self, line, termino, token):
    if termino == "D":
        nuevonodo = D_Assign()
        self.nodoactual.statements.append(nuevonodo)
        nuevonodo.padre = self.nodoactual
        self.nodoactual = nuevonodo
        self.estadoDAST = EstadoDAST.EnAsignacion
    elif termino == TokenType.T_METHOD:
        nuevonodo = Def_Fun()
        self.nodoactual.statements.append(nuevonodo)
        nuevonodo.padre = self.nodoactual
        self.nodoactual = nuevonodo
        self.estadoDAST = EstadoDAST.EnFuncion
    elif termino == (TokenType.T_RIDER or TokenType.T_MOTORCYCLE):
        nuevonodo = DefineTipoEspecial()
        self.nodoactual.statments.append(nuevonodo)
        if termino == TokenType.T_RIDER:
            otronodo = RiderInit()
            nuevonodo.statments.append(otronodo)
        else:
            otronodo = MotoInit()
            nuevonodo.statments.append(otronodo)
        self.nodoactual = nuevonodo
        self.estadoDAST = EstadoDAST.EnTipoEspecial
    elif termino == TokenType.T_IF:
        nuevonodo = IfCond()
        self.nodoactual.statements.append(nuevonodo)
        nuevonodo.padre = self.nodoactual
        self.nodoactual = nuevonodo
        self.estadoDAST = EstadoDAST.EnCondicionIf
    elif termino == TokenType.T_WHILE:
        nuevonodo = WhileCond()
        self.nodoactual.statments.append(nuevonodo)
        self.nodoactual = nodonuevo
        self.estadoDAST = EstadoDAST.EnWhile
    elif termino == TokenType.T_RETURN or termino == TokenType.T_BREAK or termino == TokenType.T_CONTINUE:
        nuevonodo = ReturnNode()
        nuevonodo.padre = self.nodoactual
        self.nodoactual.statements.append(nuevonodo)

        if termino == TokenType.T_RETURN:
            nuevonodo.type = "return"
            self.nodoactual = nuevonodo
            nodoparaExpression = Expression()
            nodoparaExpression.padre = self.nodoactual
            self.nodoactual.expr = nodoparaExpression
            self.nodoactual = nodoparaExpression
            self.estadoDAST = EstadoDAST.EnExpresionAssign

        elif termino == TokenType.T_BREAK:
            nuevonodo.type = "break"
        else:
            nuevonodo.type = "continue"

    elif termino == TokenType.T_ID:
        if self.i + 1 < len(line):
            if line[self.i + 1].token_type == TokenType.T_OPEN_PAREN:
                nuevonodo = FunCall()
                nuevonodo.id = token.value
                nuevonodo.padre = self.nodoactual
                self.nodoactual.statements.append(nuevonodo)
                self.nodoactual = nuevonodo
                self.estadoDAST = EstadoDAST.LlamadoAfuncion
            else:
                nuevonodo = Redefinition()
                self.nodoactual.statements.append(nuevonodo)
                nuevonodo.padre = self.nodoactual
                self.nodoactual = nuevonodo
                self.nodoactual.id = token.value
                self.estadoDAST = EstadoDAST.EnRedefinition
    elif termino == TokenType.T_CLOSE_BRACE:
        self.nodoactual = self.nodoactual.padre
        if isinstance(self.nodoactual, IfCond):
            if self.i + 1 == len(line):
                self.nodoactual = self.nodoactual.padre
                self.estadoDAST = EstadoDAST.EnProgram
            else:
                self.estadoDAST = EstadoDAST.EnCondicionIf
        if isinstance(self.nodoactual, Def_Fun) or isinstance(self.nodoactual, WhileCond):
            self.nodoactual = self.nodoactual.padre
            self.estadoDAST = EstadoDAST.EnProgram


def EligeTipoDdeclaracion(self, termino, token: Token, line):
    if self.estadoDAST == EstadoDAST.EnAsignacion:
        self.CreaNododAsignacion(termino, token)
    elif self.estadoDAST == EstadoDAST.EnExpresionAssign:
        self.CreaNododExpresion(termino, token, line)
    elif self.estadoDAST == EstadoDAST.EnProgram:
        self.CreaNododProgram(line, termino, token)
    elif self.estadoDAST == EstadoDAST.EnCondicionIf:
        self.CreaNododIf(termino, token)
    elif self.estadoDAST == EstadoDAST.EnFuncion:
        self.CreaNododFuncion(termino, token)
    elif self.estadoDAST == EstadoDAST.EnArgsdFuncion:
        self.CreaArgsdfun(termino, token)
    elif self.estadoDAST == EstadoDAST.EnRedefinition:
        self.CreanodoDredefinition(termino, token)
    elif self.estadoDAST == EstadoDAST.Condicion:
        self.CreaNodoCondicion(termino, token)
    elif self.estadoDAST == EstadoDAST.EnWhile:
        self.CreaNododIf(termino, token)
    elif self.estadoDAST == EstadoDAST.LlamadoAfuncion:
        self.CreanodoCall(termino, token)


def CreaNododAsignacion(self, termino, token: Token):
    if termino == TokenType.T_INT:
        self.nodoactual.typevar = VariableType.INT
    elif termino == TokenType.T_BOOL:
        self.nodoactual.typevar = VariableType.BOOL
    elif termino == TokenType.T_DOUBLE:
        self.nodoactual.typevar = VariableType.DOUBLE
    elif termino == TokenType.T_ID:
        self.nodoactual.id = token.value
    elif termino == TokenType.T_ASSIGN:
        nuevonodo = Expression()
        if not self.nodoactual.isarray:
            self.estadoDAST = EstadoDAST.EnExpresionAssign
            self.nodoactual.expr = nuevonodo
            nuevonodo.padre = self.nodoactual
            self.nodoactual = self.nodoactual.expr
        else:
            self.nodoactual.arrayvalue.append(nuevonodo)
            self.estadoDAST = EstadoDAST.EnExpresionAssign
            nuevonodo.padre = self.nodoactual
            self.nodoactual = nuevonodo

    elif termino == TokenType.T_STRING:
        self.nodoactual.typevar = VariableType.STRING
    elif termino == TokenType.T_ARRAY:
        self.nodoactual.isarray = True
    elif termino == TokenType.T_COMMA:
        nuevonodo = Expression()
        self.nodoactual.arrayvalue.append(nuevonodo)
        self.estadoDAST = EstadoDAST.EnExpresionAssign
        nuevonodo.padre = self.nodoactual
        self.nodoactual = nuevonodo
    elif termino == TokenType.T_SEMICOLON:
        self.estadoDAST = EstadoDAST.EnProgram
        self.nodoactual = self.nodoactual.padre


def CreanodoCall(self, termino, token: Token):
    if termino == "E":

        if isinstance(self.nodoactual, Expression):
            nuevonodo = NodeE()
            nuevonodo.padre = self.nodoactual.nododreconocimiento
            self.nodoactual.nododreconocimiento.args.append(nuevonodo)
            self.nodoactual.nododreconocimiento = nuevonodo
        else:
            nuevonodo = Expression()
            nuevonodo.padre = self.nodoactual
            self.nodoactual.args.append(nuevonodo)
            self.nodoactual = nuevonodo
        self.estadoDAST = EstadoDAST.EnExpresionAssign


def CreaArgsdfun(self, termino, token: Token):
    if termino == TokenType.T_INT:
        self.nodoactual.args.append([VariableType.INT])
    if termino == TokenType.T_ID:
        self.nodoactual.args[len(self.nodoactual.args) - 1].append(token.value)
    elif termino == TokenType.T_BOOL:
        self.nodoactual.args.append([VariableType.BOOL])
    elif termino == TokenType.T_DOUBLE:
        self.nodoactual.args.append([VariableType.DOUBLE])
    elif termino == TokenType.T_STRING:
        self.nodoactual.args.append([VariableType.STRING])
    elif termino == TokenType.T_CLOSE_PAREN:
        self.estadoDAST = EstadoDAST.EnFuncion


def CreanodoDredefinition(self, termino, token: Token):
    if termino == TokenType.T_ASSIGN:
        nuevonodo = Assign(self.nodoactual.id)
    elif termino == TokenType.T_ADD_AS:
        nuevonodo = AddAs(self.nodoactual.id)
    elif termino == TokenType.T_SUB_AS:
        nuevonodo = SubAs(self.nodoactual.id)
    elif termino == TokenType.T_MUL_AS:
        nuevonodo = MulAs(self.nodoactual.id)
    elif termino == TokenType.T_DIV_AS:
        nuevonodo = DivAs(self.nodoactual.id)
    elif termino == TokenType.T_MOD_AS:
        nuevonodo = ModAs(self.nodoactual.id)
    elif termino == TokenType.T_EXP_AS:
        nuevonodo = ExpAs(self.nodoactual.id)
    elif termino == TokenType.T_AND_AS:
        nuevonodo = AndAs(self.nodoactual.id)
    elif termino == TokenType.T_OR_AS:
        nuevonodo = OrAs(self.nodoactual.id)
    elif termino == TokenType.T_XOR_AS:
        nuevonodo = XorAs(self.nodoactual.id)
    elif termino == TokenType.T_SEMICOLON:
        self.estadoDAST = EstadoDAST.EnProgram
        self.nodoactual = self.nodoactual.padre
        return
    if termino != "I" and termino != "H":
        self.nodoactual.op = nuevonodo
        self.estadoDAST = EstadoDAST.EnExpresionAssign
        nodoexpression = Expression()
        self.nodoactual.expr = nodoexpression
        self.nodoactual.op.expression = nodoexpression
        nodoexpression.padre = self.nodoactual
        self.nodoactual = self.nodoactual.expr


def CreaNododFuncion(self, termino, token: Token):
    if termino == TokenType.T_INT:
        self.nodoactual.typefun = MethodType.INT
    elif termino == TokenType.T_BOOL:
        self.nodoactual.typefun = MethodType.BOOL
    elif termino == TokenType.T_DOUBLE:
        self.nodoactual.typefun = MethodType.DOUBLE
    elif termino == TokenType.T_STRING:
        self.nodoactual.typefun = MethodType.STRING
    elif termino == TokenType.T_ARRAY:
        self.nodoactual.typefun = MethodType.ARRAY
    elif termino == TokenType.T_VOID:
        self.nodoactual.typefun = MethodType.VOID
    elif termino == TokenType.T_ID:
        self.nodoactual.idfun = token.value
        self.estadoDAST = EstadoDAST.EnArgsdFuncion
    elif termino == TokenType.T_OPEN_BRACE:
        nodonuevo = Program()
        nodonuevo.padre = self.nodoactual
        self.nodoactual.body = nodonuevo
        self.nodoactual = nodonuevo
        self.nodoactual.isfuncion = True
        self.estadoDAST = EstadoDAST.EnProgram


def CreaNododIf(self, termino, token: Token):
    if termino == TokenType.T_OPEN_BRACE:
        nuevonodo = Program()
        nuevonodo.padre = self.nodoactual
        self.nodoactual.body = nuevonodo
        self.nodoactual = nuevonodo
        self.estadoDAST = EstadoDAST.EnProgram
    elif termino == TokenType.T_OPEN_PAREN:
        self.estadoDAST = EstadoDAST.Condicion
        nuevonodo = Condition()
        nuevonodo.padre = self.nodoactual
        self.nodoactual = nuevonodo
    elif termino == TokenType.T_ELIF:
        nuevonodo = IfCond()
        nuevonodo.padre = self.nodoactual
        self.nodoactual.nodoelse = nuevonodo
        self.nodoactual = nuevonodo
    elif termino == TokenType.T_ELSE:
        nuevonodo = Program()
        nuevonodo.padre = self.nodoactual
        self.nodoactual.nodoelse = nuevonodo
        self.nodoactual = nuevonodo
        self.estadoDAST = EstadoDAST.EnProgram


def CreaNodoCondicion(self, termino, token: Token):
    if termino == TokenType.T_EQ_REL:
        self.nodoactual.comparador = EqRel(self.nodoactual.expression1, self.nodoactual.expression2)
        nuevonodo = Expression()
        self.nodoactual.expression2 = nuevonodo
        nuevonodo.padre = self.nodoactual
        self.nodoactual = nuevonodo
        self.nodoactual.noderaiz = self.nodoactual.nododreconocimiento
        self.estadoDAST = EstadoDAST.EnExpresionAssign
    elif termino == TokenType.T_NEQ_REL:
        self.nodoactual.comparador = NeqRel(self.nodoactual.expression1, self.nodoactual.expression2)
        nuevonodo = Expression()
        self.nodoactual.expression2 = nuevonodo
        nuevonodo.padre = self.nodoactual
        self.nodoactual = nuevonodo
        self.nodoactual.noderaiz = self.nodoactual.nododreconocimiento
        self.estadoDAST = EstadoDAST.EnExpresionAssign
    elif termino == TokenType.T_LESS_REL:
        self.nodoactual.comparador = LessRel(self.nodoactual.expression1, self.nodoactual.expression2)
        nuevonodo = Expression()
        self.nodoactual.expression2 = nuevonodo
        nuevonodo.padre = self.nodoactual
        self.nodoactual = nuevonodo
        self.nodoactual.noderaiz = self.nodoactual.nododreconocimiento
        self.estadoDAST = EstadoDAST.EnExpresionAssign
    elif termino == TokenType.T_LEQ_REL:
        self.nodoactual.comparador = LeqRel(self.nodoactual.expression1, self.nodoactual.expression2)
        nuevonodo = Expression()
        self.nodoactual.expression2 = nuevonodo
        nuevonodo.padre = self.nodoactual
        self.nodoactual = nuevonodo
        self.nodoactual.noderaiz = self.nodoactual.nododreconocimiento
        self.estadoDAST = EstadoDAST.EnExpresionAssign
    elif termino == TokenType.T_GREAT_REL:
        self.nodoactual.comparador = GreatRel(self.nodoactual.expression1, self.nodoactual.expression2)
        nuevonodo = Expression()
        self.nodoactual.expression2 = nuevonodo
        nuevonodo.padre = self.nodoactual
        self.nodoactual = nuevonodo
        self.nodoactual.noderaiz = self.nodoactual.nododreconocimiento
        self.estadoDAST = EstadoDAST.EnExpresionAssign
    elif termino == TokenType.T_GREQ_REL:
        self.nodoactual.comparador = GreqRel(self.nodoactual.expression1, self.nodoactual.expression2)
        nuevonodo = Expression()
        self.nodoactual.expression2 = nuevonodo
        nuevonodo.padre = self.nodoactual
        self.nodoactual = nuevonodo
        self.nodoactual.noderaiz = self.nodoactual.nododreconocimiento
        self.estadoDAST = EstadoDAST.EnExpresionAssign
    elif termino == "E":
        nuevonodo = Expression()
        self.nodoactual.expression1 = nuevonodo
        nuevonodo.padre = self.nodoactual
        self.nodoactual = nuevonodo
        self.nodoactual.noderaiz = self.nodoactual.nododreconocimiento
        self.estadoDAST = EstadoDAST.EnExpresionAssign
    elif termino == TokenType.T_CLOSE_PAREN or termino == TokenType.T_OR_OP or termino == TokenType.T_AND_OP or termino == TokenType.T_XOR_OP:
        self.nodoactual.padre.conditions.append(self.nodoactual)
        if termino == TokenType.T_CLOSE_PAREN:
            self.estadoDAST = EstadoDAST.EnCondicionIf
            self.nodoactual = self.nodoactual.padre
        else:

            if termino == TokenType.T_OR_OP:
                self.nodoactual.padre.operadoresbinarios.append(OrOp(None, None))
            elif termino == TokenType.T_AND_OP:
                self.nodoactual.padre.operadoresbinarios.append(AndOp(None, None))
            elif termino == TokenType.T_XOR_OP:
                self.nodoactual.padre.operadoresbinarios.append(XorOp(None, None))
            nodopadre = self.nodoactual.padre
            self.estadoDAST = EstadoDAST.EnExpresionAssign
            self.nodoactual = Condition()
            self.nodoactual.padre = nodopadre

            nuevonodo = Expression()
            self.nodoactual.expression1 = nuevonodo
            nuevonodo.padre = self.nodoactual
            self.nodoactual = nuevonodo
            self.nodoactual.noderaiz = self.nodoactual.nododreconocimiento


def CreaNododExpresion(self, termino, token: Token, line):
    if termino != "G":

        # if termino==TokenType.T_CLOSE_BRACKET and line[self.i-1]==TokenType.T_ASSIGN:

        if termino == TokenType.T_ADD_OP:
            nuevonodo = NodeAdd()
        elif termino == TokenType.T_SUB_OP:
            nuevonodo = NodeSub()
        elif termino == TokenType.T_MUL_OP:
            nuevonodo = NodeMult()
        elif termino == TokenType.T_DIV_OP:
            nuevonodo = NodeDiv()
        elif termino == TokenType.T_MOD_OP:
            nuevonodo = NodeMod()
        elif termino == TokenType.T_EXP_OP:
            nuevonodo = NodeExp()
        elif termino == TokenType.T_COMMA:
            self.estadoDAST = EstadoDAST.LlamadoAfuncion
            if isinstance(self.nodoactual.padre, FunCall):
                self.nodoactual = self.nodoactual.padre
            return
        elif termino == "B":
            nuevonodo = NodeB()
        elif termino == "M":
            nuevonodo = NodeM()
        elif termino == "E":
            nuevonodo = NodeE()
        elif termino == "X":
            nuevonodo = NodeX()
        elif termino == "Y":
            nuevonodo = NodeY()
        elif termino == "e":
            nuevonodo = Nodepsilon()
        elif termino == "Q":
            nuevonodo = NodeQ()
        elif termino == TokenType.T_OPEN_PAREN or termino == TokenType.T_CLOSE_PAREN:
            if termino == TokenType.T_CLOSE_PAREN and isinstance(self.nodoactual, FunCall):
                self.nodoactual = self.nodoactual.padre
                return
            elif termino == TokenType.T_CLOSE_PAREN and isinstance(self.nodoactual.nododreconocimiento, FunCall):
                self.nodoactual.nododreconocimiento = self.nodoactual.nododreconocimiento.padre
                return
            else:
                nuevonodo = Nodepsilon()
        elif termino == TokenType.T_D_VALUE or termino == TokenType.T_I_VALUE or termino == TokenType.T_S_VALUE or termino == TokenType.T_FALSE or termino == TokenType.T_TRUE:
            nuevonodo = Val(token)
        elif termino == TokenType.T_ID:
            if len(line) - 1 == self.i:
                nuevonodo = Variable(token)
            elif line[self.i + 1].token_type == TokenType.T_OPEN_PAREN:
                nuevonodo = FunCall()
                nuevonodo.id = token.value
                self.estadoDAST = EstadoDAST.LlamadoAfuncion
            else:
                nuevonodo = Variable(token)
        if termino != TokenType.T_OPEN_BRACKET and termino != "U":
            if isinstance(self.nodoactual.nododreconocimiento, NodeE) and isinstance(nuevonodo, NodeE):
                self.nodoactual.nododreconocimiento = nuevonodo
                self.nodoactual.noderaiz = nuevonodo
            elif termino != "A" and termino != "Z" and termino != "U":
                nuevonodo.padre = self.nodoactual.nododreconocimiento
                self.nodoactual.nododreconocimiento.hijos.append(nuevonodo)
                if termino == "E" or termino == "B" or termino == "M" or termino == "X" or termino == "Y" or termino == "Q" or isinstance(
                        nuevonodo, FunCall):
                    self.nodoactual.nododreconocimiento = nuevonodo


def RectificaEstado(self):
    if isinstance(self.nodoactual.padre, Condition):
        self.estadoDAST = EstadoDAST.Condicion  # Metodo para subir en el ast
    elif isinstance(self.nodoactual.padre, D_Assign):
        self.estadoDAST = EstadoDAST.EnAsignacion
    elif isinstance(self.nodoactual.padre, Redefinition):
        self.estadoDAST = EstadoDAST.EnRedefinition
    # Metodo para subir en el ast
    elif isinstance(self.nodoactual.padre, Program):
        self.estadoDAST = EstadoDAST.EnProgram  # Metodo para subir en el ast
    elif isinstance(self.nodoactual.padre, ReturnNode):
        self.estadoDAST = EstadoDAST.EnProgram
    elif isinstance(self.nodoactual.padre, FunCall):
        self.estadoDAST = EstadoDAST.LlamadoAfuncion