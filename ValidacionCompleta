    def CreaNododExpresion(self,termino,token:Token,line):
        
      if termino!="G"  :
        if termino==TokenType.T_ADD_OP:
            nuevonodo=NodeAdd()
        elif termino==TokenType.T_SUB_OP:
            nuevonodo=NodeSub()
        elif termino==TokenType.T_MUL_OP:
            nuevonodo=NodeMult()
        elif termino==TokenType.T_DIV_OP:
            nuevonodo=NodeDiv()
        elif termino==TokenType.T_MOD_OP:
            nuevonodo=NodeMod()
        elif termino==TokenType.T_EXP_OP:
            nuevonodo=NodeExp()
        elif termino==TokenType.T_COMMA:
             self.estadoDAST=EstadoDAST.LlamadoAfuncion
             return
        elif termino=="B":
            nuevonodo=NodeB()            
        elif termino=="M":
            nuevonodo=NodeM()            
        elif termino=="E":
           nuevonodo=NodeE()           
        elif termino=="X":
           nuevonodo=NodeX() 
        elif termino=="Y":
           nuevonodo=NodeY() 
        elif termino=="e":
            nuevonodo=Nodepsilon()
        elif termino=="Q":
            nuevonodo=NodeQ()
        elif termino==TokenType.T_OPEN_PAREN or termino==TokenType.T_CLOSE_PAREN:
            if termino==TokenType.T_CLOSE_PAREN and isinstance(self.nodoactual.nododreconocimiento,FunCall):
                self.nodoactual.nododreconocimiento = self.nodoactual.nododreconocimiento.padre 
                return
            else :
             nuevonodo=Nodepsilon()
        elif termino== TokenType.T_D_VALUE or termino==TokenType.T_I_VALUE or termino==TokenType.T_S_VALUE or termino==TokenType.T_FALSE or termino==TokenType.T_TRUE  :
            nuevonodo=Val(token)
        elif termino==TokenType.T_ID:
             if line[self.i+1].token_type==TokenType.T_OPEN_PAREN:
                 nuevonodo=FunCall()
                 nuevonodo.id= token.value
                 self.estadoDAST=EstadoDAST.LlamadoAfuncion
             else:  
                 nuevonodo=Variable(token)
        if isinstance(self.nodoactual.nododreconocimiento,NodeE) and isinstance(nuevonodo,NodeE):
            self.nodoactual.nododreconocimiento=nuevonodo
            self.nodoactual.noderaiz=nuevonodo
        elif termino!="A" and termino!="Z" and termino!="U":
            nuevonodo.padre=self.nodoactual.nododreconocimiento
            self.nodoactual.nododreconocimiento.hijos.append(nuevonodo)
            if termino == "E" or termino=="B" or termino=="M"or termino=="X" or termino=="Y" or termino=="Q" or isinstance(nuevonodo,FunCall) :
             self.nodoactual.nododreconocimiento=nuevonodo



 def CreanodoCall(self,termino,token:Token):
        if termino=="E":
            nuevonodo= NodeE()
            nuevonodo.padre=self.nodoactual.nododreconocimiento
            self.nodoactual.nododreconocimiento.args.append(nuevonodo)
            self.nodoactual.nododreconocimiento=nuevonodo
            self.estadoDAST=EstadoDAST.EnExpresionAssign
            
 def EligeTipoDdeclaracion(self,termino,token:Token,line):
        if self.estadoDAST==EstadoDAST.EnAsignacion:
            self.CreaNododAsignacion(termino,token)
        elif self.estadoDAST==EstadoDAST.EnExpresionAssign:
            self.CreaNododExpresion(termino,token,line)
        elif self.estadoDAST==EstadoDAST.EnProgram:
            self.CreaNododProgram(termino,token)
        elif self.estadoDAST==EstadoDAST.EnCondicionIf:
            self.CreaNododIf(termino,token)
        elif self.estadoDAST==EstadoDAST.EnFuncion:
            self.CreaNododFuncion(termino,token)
        elif self.estadoDAST==EstadoDAST.EnArgsdFuncion:
            self.CreaArgsdfun(termino,token)
        elif self.estadoDAST==EstadoDAST.EnRedefinition:
            self.CreanodoDredefinition(termino,token)
        elif self.estadoDAST==EstadoDAST.Condicion:
            self.CreaNodoCondicion(termino,token)
        elif self.estadoDAST==EstadoDAST.EnWhile:
            self.CreaNododIf(termino,token)
        elif self.estadoDAST==EstadoDAST.LlamadoAfuncion:
            self.CreanodoCall(termino,token)
            
    class Expression(Node):
    def __init__(self):
         self.nododreconocimiento= NodeE()
         self.noderaiz=NodeE()

    def validate(self,context:Context):
        if not self.noderaiz.validate(context):
            return False
        return False

class D_Assign(Statement):
    typevar: VariableType
    id : str
    expr : Expression
    isarray: bool 

    def validate(self, context: Context) -> bool:
        if not self.expr.validate(context):
           return False
        if not context.define_var(id):
            return False
       
        return False

    @staticmethod
    def type() -> str:
        return "DecAssign"

class Redefinition(Statement):
     def __init__(self):
       self.id=None
       self.op=None
       self.expr:Expression=None

     def validate(self, context: Context) -> bool:
         if not self.expr.validate():
             return False 
         
         if not context.check_var(self.id):
              return False
         
         return True


     @staticmethod
     def type() -> str:
        return "Redef"
        
        
class Def_Fun(Statement):
    typefun: MethodType
    idfun: str
    args:list(list())=[]
    body=Program()


    def validate(self, context : Context) -> bool:
        nuevocontext= context.crearnuevocontexto(self.context)

        for arg in args:
           if not nuevocontext.define_var(arg):
               return False

        if not body.validate(nuevocontexto):
            return False

        nuevocontext.define_fun(idfun,args)

    @staticmethod
    def type() -> str:
        return "DefFun"



class Condition(Node):
     def __init__(self):
       self.expression1=Expression()
       self.expression2=Expression()
       self.comparador:Rel=None

     def validate (self,context:Context):
         return self.expression1.validate(context) and self.expression2.validate(context)


     @staticmethod
     def type() -> str:
        return "Conditional"

class IfCond(Statement):
    def __init__(self):
        self.operadoresbinarios=[]
        self.conditions:list(Condition)=[]
        self.body=Program()
        self.nodoelse=None

    def validate (self,context:Context):
        
        if self.nodoelse!=None:
          if not self.nodoelse.validate(context):
            return False
        
        if not self.body.validate(context):
            return False
        
        for condition in self.conditions:
             if not condition.validate(context):
                 return False

        return True

    @staticmethod
    def type() -> str:
        return "If"

class WhileCond(Statement):
    def __init__(self):
        self.operadoresbinarios=[]
        self.conditions:list(Condition)=[]
        self.body=Program()
 
    def validate (self,context:Context):
        if not self.body.validate(context):
            return False
        
        for condition in self.conditions:
             if not condition.validate(context):
                 return False

        return True

    @staticmethod
    def type() -> str:
        return "While"
        
class BinOp(Op):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(right_node)
        self.left_node = left_node

    def validate(self,context:Context):
        return self.left_node.validate(context) and self.right_node.validate(context)

    def eval(self, variables: dict):
        left = self.left_node.eval(variables)
        right = self.right_node.eval(variables)
        if is_error(left):
            return left
        if is_error(right):
            return right
        return self.operation(left, right)

    def operation(self, left, right):
        return None

    def __repr__(self) -> str:
        return "{}({}, {})".format(self.type(), self.left_node, self.right_node)

    @staticmethod
    def type() -> str:
        return "BIN_OP"
        
        
 class Val(Node):
    def __init__(self,val):
     self.val=val

    def validate(context:Context):
        return True

    @staticmethod
    def type() -> str:
        return "EXP"

class Variable(Node):
    padre = None
    def __init__(self,token:Token):
        self.idvar= token.value
    
    def validate(self,context:Context):
        return context.check_var(self.idvar)

    @staticmethod
    def type() -> str:
        return "Variable"

class FunCall(Node):
    id: str
    args:list()=[]


    def validate (self,context:Context)->bool:
       for expr in self.args:
           if not expr.validate(context):
               return False

       return context.check_fun(self.id,len(self.args))

    @staticmethod
    def type() -> str:
        return "FunCall"

class NodeE(Node):
    def __init__(self):
    
     self.padre = None
     self.hijos = list() 
     self.ast=None

    def refreshAST(self):
     if len(self.hijos)>0:
        self.ast = self.hijos[1].ast 

    def validate(self,context:Context):
        if not self.ast.validate(context):
           return False
        return False
