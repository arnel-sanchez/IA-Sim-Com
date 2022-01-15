 def CreaNododProgram(self,termino):
        if termino=="D":
            nuevonodo = D_Assign()
            self.nodoactual.statments.append(nuevonodo)
            self.nodoactual=nuevonodo
            self.estadoDAST=EstadoDAST.EnAsignacion
        elif termino==TokenType.T_METHOD:
            nuevonodo= Def_Fun()
            self.nodoactual.statments.append(nuevonodo)
            self.nodoactual=nuevonodo
            self.estadoDAST=EstadoDAST.EnFuncion
        elif termino== (TokenType.T_RIDER or TokenType.T_MOTORCYCLE):
            nuevonodo= DefineTipoEspecial()
            self.nodoactual.statments.append(nuevonodo)
            if termino == TokenType.T_RIDER:
                otronodo=RiderInit() 
                nuevonodo.statments.append(otronodo)                
            else:
                otronodo=MotoInit() 
                nuevonodo.statments.append(otronodo)
            self.nodoactual=nuevonodo
            self.estadoDAST=EstadoDAST.EnTipoEspecial
        elif termino== TokenType.T_IF :
            nuevonodo= IfCond()
            self.nodoactual.statments.append(nuevonodo)
            self.nodoactual=nodonuevo
            self.estadoDAST=EstadoDAST.EnCondicionIf
        elif termino == TokenType.T_WHILE :
            nuevonodo = WhileCond()
            self.nodoactual.statments.append(nuevonodo)
            self.nodoactual=nodonuevo
            self.estadoDAST=EstadoDAST.EnWhile
    

    def EligeTipoDdeclaracion(self,termino,token:Token):
        if self.estadoDAST==EstadoDAST.EnAsignacion:
            self.CreaNododAsignacion(termino,token)
        elif self.estadoDAST==EstadoDAST.EnExpresionAssign:
            self.CreaNododAsignacion(termino,token)
        elif self.estadoDAST==EstadoDAST.EnProgram:
            self.CreaNododProgram(termino)
        elif self.estadoDAST==EstadoDAST.EnCondicionIf:
            self.CreaNododIf(termino)
        elif self.estadoDAST==EstadoDAST.EnFuncion:
            self.CreaNododFuncion(termino)
        elif self.estadoDAST==EstadoDAST.EnArgsdFuncion:
            self.CreaArgsdfun(termino,token)
    
    def CreaNododAsignacion(self,termino,token:Token):
        if termino==TokenType.T_INT :
            self.nodoactual.type=VariableType.INT
        elif termino==TokenType.T_BOOL :
            self.nodoactual.type=VariableType.BOOL
        elif termino==TokenType.T_DOUBLE :
            self.nodoactual.type=VariableType.DOUBLE
        elif termino==TokenType.T_ID :
             self.nodoactual.id = token.value
        elif termino==TokenType.T_ASSIGN :
            self.estadoAST=EstadoDAST.EnExpresionAssign
        elif termino==TokenType.T_STRING:
            self.nodoactual.type=VariableType.STRING
        elif termino==TokenType.T_ARRAY:
            self.nodoactual.isarray=True
       
    def CreaArgsdfun(self,termino,token:Token):
        if termino==TokenType.T_INT :
            self.nodoactual.args.append((VariableType.INT,""))
        if termino==TokenType.T_ID :
            self.nodoactual.args[len(args)-1][1] = token.value
        elif termino==TokenType.T_BOOL :
            self.nodoactual.args.append((VariableType.BOOL,""))
        elif termino==TokenType.T_DOUBLE :
            self.nodoactual.args.append((VariableType.DOUBLE,""))
        elif termino==TokenType.T_STRING:
            self.nodoactual.args.append((VariableType.STRING,""))
        elif termino==TokenType.T_CLOSE_PAREN:
            self.estadoDAST=EstadoDAST.EnFuncion

    def CreaNododFuncion(self,termino,token:Token):
        if termino == TokenType.T_INT  :
            self.nodoactual.typefun= MethodType.INT
        elif termino==TokenType.T_BOOL :
            self.nodoactual.typefun= MethodType.BOOL
        elif termino==TokenType.T_DOUBLE :
            self.nodoactual.typefun= MethodType.DOUBLE
        elif termino==TokenType.T_STRING:
            self.nodoactual.typefun= MethodType.STRING
        elif termino==TokenType.T_ARRAY:
           self.nodoactual.typefun= MethodType.ARRAY
        elif termino==TokenType.T_VOID:
           self.nodoactual.typefun= MethodType.VOID
        elif termino==TokenType.T_ID :
           self.nodoactual.idfun=token.value
           self.estadoDAST=EstadoDAST.EnArgsdFuncion
        elif termino==TokenType.T_OPEN_BRACE :
            nodonuevo= BodyDFun()
            self.nodoactual.body=nodonuevo
            self.nodoactual=nodonuevo
            self.estadoDAST=EstadoDAST.EnProgram
            
    def CreaNododIf(self,termino,token:Token):
        if self.estadoAST==EstadoDAST.EnCondicionIf:
           if termino == TokenType.T_OPEN_BRACE:
               self.estadoDAST=EstadoDAST.EnBodyIf
               nodonuevo=BodyDIf()
               self.nodoactual.body=nodonuevo
               self.nodoactual=nodonuevo
               self.estadoDAST=EstadoDAST.EnProgram
       
           
    def CreaNododExpresion(self,termino):
        #Falta Implementarlo
        return 3

 

class VariableType(Enum):
    STRING = 0
    INT = 1
    DOUBLE = 2
    BOOL = 3
    ARRAY = 4

class MethodType(Enum):
    VOID = 0
    STRING = 1
    INT = 2
    DOUBLE = 3
    BOOL = 4
    ARRAY = 5

class Program(Node): 
    statements:List[Statement]

    def validate():
        for dec in statments:
            if not dec.validate():
                return False
        return True
    
    @staticmethod
    def type() -> str:
        return "Program"

class Statement(Node):

  def type() -> str:
        return "Statment"
   
class D_Assign(Statement):
    typevar: VariableType
    id : str
    expr : Expression
    isarray: bool 

    def validate(self, variables: dict) -> bool:
       return #

    @staticmethod
    def type() -> str:
        return "DecAssign"

class Redefinition(Statement):
   
    def validate(self, variables: dict) -> bool:
       return #

    @staticmethod
    def type() -> str:
        return "Redef"

class BodyDFun(Program):

     @staticmethod
     def type() -> str:
        return "CuerpoDFun"

class BodyDIf(Program):

     @staticmethod
     def type() -> str:
        return "CuerpoDIf"

class Def_Fun(Statement):
    typefun: MethodType
    idfun: str
    args:list[(VariableType,str)]
    body: BodyDFun

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

class IfCond(Conditional):
    condition: Condition
    body:BodyDIf

    @staticmethod
    def type() -> str:
        return "If"

class Context:
     
    variables=dict()
    funciones=dict()
    errors=list()
    contextPadre = Null 

    def check_var(self,var:str)->bool :
         varContain = self.variables.get(var,"NoEsta")
         if varContain != "NoEsta":
             return True
         else :
             while self.contextPadre!=Null:
                 self=self.contextPadre
                 varContain = self.variables.get(var,"NoEsta")
                 if varContain != "NoEsta":
                     return True
             return False

    def check_fun(self,fun:str,args:int)->bool :
         funContain = self.funciones.get(fun,"NoEsta")
         if funContain != "NoEsta":
             return True
         else :
             while self.contextPadre!=Null:
                 self=self.contextPadre
                 funContain = self.funciones.get(fun,"NoEsta")
                 if funContain != "NoEsta":
                     return True
             return False
    def define_fun(self,fun:str,args:List[str])->bool :
        funContain = self.funciones.get(fun,"NoEsta")
        if funContain != "NoEsta":
            self.errors.append("ya existe una funcion con este nombre en este contexto")
        else:
            self.funciones.setdefault(fun,len(args))
        return True
    def define_var(self,var:str)->bool :
        varContain = self.variables.get(var,"NoEsta")
        if varContain != "NoEsta":
            self.errors.append("ya existe una variable con este nombre en este contexto")
        else:
            self.variables.setdefault(var)
        return True
    def crearnuevocontexto(self,context:Context)->Context :
          nuevocontext=Context()
          nuevocontext.contextPadre=context

          return nuevocontext
