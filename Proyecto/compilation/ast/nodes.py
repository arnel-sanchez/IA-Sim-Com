from compilation.tokens import Token, TokenType
from compilation.errors import Error

class Node:

    def eval(self, variables: dict):
        return None

    def __repr__(self) -> str:
        return "NODE()"
       
class Call(Node):
     def __init__(self,token:Token):
      self.id=token.value

class Statement(Node):

  def type() -> str:
        return "Statment"

class Program(Node): 
    def __init__(self):
      self.isfuncion:bool=False
      self.statements: list()=[]
      self.padre:Node=None
      self.listaDReturns:list()=[]

    def validate(self,context:Context):
        for dec in self.statements:
            if not dec.validate(context):
                return False


        return True
    
    def checktype(self,context:Context):        
           countReturn=0
           for statement in self.statements:   
               if isinstance(statement,ReturnNode):
                   countReturn+=1
               if not statement.checktype(context):
                   return False
           return True
        

        


    @staticmethod
    def type() -> str:
        return "Program"
    statements= list()

    def validate():
        for dec in statments:
            if not dec.validate():
                return False
        return True
    
    @staticmethod
    def type() -> str:
        return "Program"

class Expression(Node):
    def __init__(self):
         self.nododreconocimiento= NodeE()
         self.noderaiz=NodeE()

    def checktype(self,context:Context):
        return self.noderaiz.checktype(context)

    def validate(self,context:Context):
        if not self.noderaiz.validate(context):
            return False
        return True

class D_Assign(Statement):
    typevar: VariableType
    id : str
    expr : Expression=None
    isarray: bool=False
    arrayvalue:list()=[]

    def validate(self, context: Context) -> bool:
       if not self.isarray:
        if not self.expr.validate(context):
           return False
        if not context.define_var(self.id,self.typevar):
            return False
       else :
           for expresion in self.arrayvalue:
              if not expresion.validate(context):
                 return False
       return True

    def checktype(self,context:Context):
        if not self.isarray:
            typeExpression=self.expr.checktype(context)
            type= normaliza(self.typevar)
            if typeExpression==type:
                return True
            return False
        else:
            for expression in arrayvalue:
                typeExpression=expression.checktype(context)
                if typeExpression!=typevar:
                 return False
            return True

    

    @staticmethod
    def type() -> str:
        return "DecAssign"

class ReturnNode(Statement):
    type=""
    expr:Expression= Expression()
    padre=None

    def validate(self,context:Context):
            if not self.expr.validate(context):
                return False
            return True

    def checktype(self,context:Context):
       if  normaliza(self.padre.padre.typefun)==self.expr.checktype(context):
           return True
       return False
           
class Redefinition(Statement):
     def __init__(self):
       self.id=None
       self.op=None
       self.expr:Expression=None

     def validate(self, context: Context) -> bool:
         if not self.expr.validate(context):
             return False 
         
         if not context.check_var(self.id):
              return False
         
         return True

     def checktype(self,context:Context):
          return self.op.checktype(context)         
           

     @staticmethod
     def type() -> str:
        return "Redef"
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
    body:Program
    nuevocontext:Context=None
    

    def validate(self, context : Context) -> bool:
        self.nuevocontext= context.crearnuevocontexto()

        for arg in self.args:
           if not self.nuevocontext.define_var(arg[1],arg[0]):
               return False

        if not self.body.validate(self.nuevocontext):
            return False

        self.nuevocontext.define_fun(idfun,typefun,args)

    def checktype(self,context:Context):
        return self.body.checktype(self.nuevocontext)


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

     def checktype(self,context:Context):
        if self.expression2.nododreconocimiento.ast==None:
            if self.expression1.checktype(context)!="bool":
                return False
            else : return True

        elif self.expression1.checktype(context)==self.expression2.checktype(context):
            return True
        else:
            return False

     @staticmethod
     def type() -> str:
        return "Conditional"

class IfCond(Statement):
    def __init__(self):
        self.operadoresbinarios=[]
        self.conditions:list(Condition)=[]
        self.body=Program()
        self.nodoelse=None
        self.nuevocontexto:Context=None

    def validate (self,context:Context):
        
        for condition in self.conditions:
             if not condition.validate(context):
                 return False
         
        self.nuevocontexto=context.crearnuevocontexto()

        if not self.body.validate(self.nuevocontexto):
            return False

        if self.nodoelse!=None:
          if not self.nodoelse.validate(self.nuevocontexto):
            return False
        return True

    def checktype(self,context:Context):
        for condition in self.conditions:
            if  not condition.checktype(context):
                return False
        
        if not self.body.checktype(self.nuevocontexto):
            return False
        
        if self.nodoelse!=None:
          if not self.nodoelse.checktype(self.nuevocontexto):
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
        self.nuevocontexto=None

    def validate (self,context:Context):
              
        for condition in self.conditions:
             if not condition.validate(context):
                 return False
             
        self.nuevocontexto=context.crearnuevocontexto()

        if not self.body.validate(self.nuevocontexto):
            return False

        return True


    def checktype(self,context:Context):
        for condition in self.conditions:
            if  not condition.checktype(context):
                return False

        if not self.body.checktype(self.nuevocontexto):
            return False
        return True

    @staticmethod
    def type() -> str:
        return "While"
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
         
class NodeE(Node):
    def __init__(self):    
     self.padre = None
     self.hijos = list() 
     self.ast=None

    def refreshAST(self):
     if len(self.hijos)>0:
        self.ast = self.hijos[1].ast 

    def checktype(self,context:Context):
        return self.ast.checktype(context)

    def validate(self,context:Context):
        if not self.ast.validate(context):
           return False
        return True

class NodeB(Node):
   def __init__(self):
    self.padre = None
    self.hijos= list()  
    self.ast = None 
   
   def refreshAST(self):
    if len(self.hijos)==2:
        self.ast=self.hijos[1].ast
    
class NodeX(Node):
    def __init__(self):
     self.padre = None
     self.hijos= list()
     self.ast=None

    def refreshAST(self):
     if len(self.hijos)==3:
       if isinstance(self.hijos[0],NodeAdd):
          if isinstance(self.padre,NodeX):           
            self.ast:Node = AddOp(self.padre.hijos[1].ast,self.hijos[2].ast)
          else:
             self.ast:Node = AddOp(self.padre.hijos[0].ast,self.hijos[2].ast)
       elif isinstance(self.hijos[0],NodeSub):
            if isinstance(self.padre,NodeX):           
             self.ast:Node = SubOp(self.padre.hijos[1].ast,self.hijos[2].ast)
            else:
             self.ast:Node = SubOp(self.padre.hijos[0].ast,self.hijos[2].ast)
    
     elif len(self.hijos)==0:
             if isinstance(self.padre,NodeX):           
                self.ast:Node = self.padre.hijos[1].ast
             else:
                self.ast:Node = self.padre.hijos[0].ast

class NodeM(Node):
   def __init__(self, *args, **kwargs):
    self.padre = None
    self.hijos= list()  
    self.ast=None

   def refreshAST(self):
    if len(self.hijos)==3:
        self.ast=self.hijos[1].ast
    elif len(self.hijos)==1:
         self.ast= self.hijos[0].ast
    else :
        self.ast = None

class NodeY:
    def __init__(self):
     self.ast=None
     self.padre= None
     self.hijos= list()

    def refreshAST(self):
     if len(self.hijos)==3:
       if isinstance(self.hijos[0],NodeMult):
          if isinstance(self.padre,NodeY):           
            self.ast:Node = MulOp(self.padre.hijos[1].ast,self.hijos[2].ast)
          else:
             self.ast:Node = MulOp(self.padre.hijos[0].ast,self.hijos[2].ast)
       elif isinstance(self.hijos[0],NodeDiv):
            if isinstance(self.padre,NodeY):           
             self.ast:Node = DivOp(self.padre.hijos[1].ast,self.hijos[2].ast)
            else:
             self.ast:Node = DivOp(self.padre.hijos[0].ast,self.hijos[2].ast)
       elif isinstance(self.hijos[0],NodeMod):
             if isinstance(self.padre,NodeY):           
               self.ast:Node = ModOp(self.padre.hijos[1].ast,self.hijos[2].ast)
             else:
              self.ast:Node = ModOp(self.padre.hijos[0].ast,self.hijos[2].ast)
       elif isinstance(self.hijos[0],NodeExp):
             if isinstance(self.padre,NodeY):           
               self.ast:Node = ExpOp(self.padre.hijos[1].ast,self.hijos[2].ast)
             else:
               self.ast:Node = ExpOp(self.padre.hijos[0].ast,self.hijos[2].ast)
    
     elif len(self.hijos)==0:
             if isinstance(self.padre,NodeY):           
                self.ast = self.padre.hijos[1].ast
             else:
                self.ast = self.padre.hijos[0].ast
               

                


                

              

    def __init__(self):
     self.ast=None
     self.padre= None
     self.hijos= list()

    def refreshAST(self):
     if len(self.hijos)==3:
       if isinstance(self.hijos[0],NodeMult):
          if isinstance(self.padre,NodeY):           
            self.ast:Node = MulOp(self.padre.hijos[1].ast,self.hijos[2].ast)
          else:
             self.ast:Node = MulOp(self.padre.hijos[0].ast,self.hijos[2].ast)
       elif isinstance(self.hijos[0],NodeDiv):
            if isinstance(self.padre,NodeY):           
             self.ast:Node = DivOp(self.padre.hijos[1].ast,self.hijos[2].ast)
            else:
             self.ast:Node = DivOp(self.padre.hijos[0].ast,self.hijos[2].ast)
       elif isinstance(self.hijos[0],NodeMod):
             if isinstance(self.padre,NodeY):           
               self.ast:Node = ModOp(self.padre.hijos[1].ast,self.hijos[2].ast)
             else:
              self.ast:Node = ModOp(self.padre.hijos[0].ast,self.hijos[2].ast)
       elif isinstance(self.hijos[0],NodeExp):
             if isinstance(self.padre,NodeY):           
               self.ast:Node = ExpOp(self.padre.hijos[1].ast,self.hijos[2].ast)
             else:
               self.ast:Node = ExpOp(self.padre.hijos[0].ast,self.hijos[2].ast)
    
     elif len(self.hijos)==0:
             if isinstance(self.padre,NodeY):           
                self.ast = self.padre.hijos[1].ast
             else:
                self.ast = self.padre.hijos[0].ast

class NodeQ(Node):
    def __init__(self):
    
     self.padre = None
     self.hijos=list()
     self.ast=None

    def refreshAST(self):
      if len(self.hijos)==1:
         self.ast=self.hijos[0]

class Nodepsilon(Node):
    padre = None
    
    @staticmethod
    def type() -> str:
        return "EXP"

class Val(Node):
    def __init__(self,val):
     self.val=val

    def validate(self,context:Context):
        return True

    def checktype (self,context:Context): 
        if self.val.token_type==TokenType.T_I_VALUE:
            return "int"
        if self.val.token_type==TokenType.T_DOUBLE:
            return "double"
        if self.val.token_type==TokenType.T_FALSE or TokenType.T_TRUE:
            return "bool"
        if self.val.token_type==TokenType.T_S_VALUE:
            return "str"
        

    @staticmethod
    def type() -> str:
        return "EXP"

class Variable(Node):
    padre = None
    def __init__(self,token:Token):
        self.idvar= token.value
    
    def validate(self,context:Context):
        return context.check_var(self.idvar)

    def checktype (self,context:Context):
        type =context.gettypevar(self.idvar)
        if type==VariableType.INT:
          return "int"
        if type==VariableType.BOOL:
          return "bool"
        if type==VariableType.DOUBLE:
          return "double"
        if type==VariableType.STRING:
          return "str"


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

    def checktype (self,context:Context):
        type=context.gettypefun(self.id)
        if type==MethodType.INT:
          return "int"
        if type==MethodType.BOOL:
          return "bool"
        if type==MethodType.DOUBLE:
          return "double"
        if type==MethodType.STRING:
          return "str"

    @staticmethod
    def type() -> str:
        return "FunCall"

class NodeMult(Node):
    @staticmethod
    def type() -> str:
        return "MUL"
class NodeDiv(Node): 

    @staticmethod
    def type() -> str:
        return "DIV"

class NodeMod(Node):
    

    @staticmethod
    def type() -> str:
        return "MOD"

class NodeExp(Node):
    
    @staticmethod
    def type() -> str:
        return "EXP"

class NodeAdd(Node):
  

   @staticmethod
   def type() -> str:
        return "ADD"

class NodeSub(Node):

    @staticmethod
    def type() -> str:
        return "SUB"
