from compilation.tokens import Token, TokenType
from compilation.errors import *
from compilation.context import Context
from compilation.enums import *



class NodeType(Enum):
    STRING = 0
    INT = 1
    DOUBLE = 2
    BOOL = 3
    ARRAY = 4
    OTHER = 5


def normaliza(typevar):
        if typevar==VariableType.INT or typevar==MethodType.INT:
          return "int"
        if typevar==VariableType.BOOL or typevar==MethodType.BOOL:
          return "bool"
        if typevar==VariableType.DOUBLE or typevar==MethodType.DOUBLE:
          return "double"
        if typevar==VariableType.STRING or typevar==MethodType.STRING:
          return "str"
        if typevar==MethodType.VOID:
            return "void"


class Node:
    def validate(self, variables: dict):
        return True

    #def type(self) -> NodeType:
     #   return NodeType.OTHER

    def eval(self, variables: dict):
        return None

    def __repr__(self) -> str:
        return "NODE()"


def verificatealwaysReturn(dec):
    for statement in dec.body.statements:
         if isinstance(statement,ReturnNode):
             if dec.nodoelse==None:
                 return True
             elif isinstance(dec.nodoelse,IfCond):
                 if verificatealwaysReturn(dec.nodoelse):
                     return True
             elif isinstance(dec.nodoelse,Program):
                   for statementdprogram in dec.nodoelse.statements:
                       if isinstance(statementdprogram,ReturnNode):
                           return True 
                       elif isinstance(statementdprogram,IfCond):
                             if verificatealwaysReturn(statementdprogram):  
                                 return True
         elif isinstance(statement,IfCond):
             if verificatealwaysReturn(statement):
                 return True
    return False

class Statement(Node):

  def type() -> str:
        return "Statment"

class Program(Node): 
    def __init__(self):
      self.isfuncion:bool=False
      self.statements: list()=[]
      self.padre:Node=None
      self.listaDReturns:list()=[]
      self.token=None

    def validate(self,context:Context):
        
        if isinstance(self.padre,WhileCond):
         for statement in self.statements:
             if isinstance(statement,Def_Fun):                 
                 return False #Error ,No puede definir una funcion dentro de un while
             elif isinstance(statement,RiderNode) or isinstance(statement,MotorcicleNode):                 
                 return False #Error ,No puede definir un tipo especial dentro de un while
                 #if isinstance(statement,Redefinition) or isinstance(statement,D_Assign) or isinstance(statement,WhileCond) or isinstance(statement,IfCond) or isinstance(statement,FunCall):  #estas son las declaraciones que pueden estar en cualquier ambito
             validationstatement=statement.validate(context)
             if not isinstance(validationstatement,bool):
                return validationstatement
             
        elif isinstance(self.padre,IfCond):
         for statement in self.statements:
             if isinstance(statement,Def_Fun):
                return False #Error ,No puede definir una funcion dentro de un If
             elif isinstance(statement,RiderNode) or isinstance(statement,MotorcicleNode):                 
                 return False #Error ,No puede definir un tipo especial dentro de un if
             elif isinstance(statement,ReturnNode) and (statement.type=="continue"or statement.type=="break"):
                if context.enwhile==None:
                  return IncorrectCallError("This token is incorrect, it is not within a while scope","",self.token.line,self.token.column)
                 #Error ,Esta declaracion no es valida dentro de un If
                 #if isinstance(statement,Redefinition) or isinstance(statement,D_Assign) or isinstance(statement,WhileCond) or isinstance(statement,IfCond) or isinstance(statement,FunCall):  #estas son las declaraciones que pueden estar en cualquier ambito
             validationstatement=statement.validate(context)
             if not isinstance(validationstatement,bool):
                return validationstatement
        elif isinstance(self.padre,Def_Fun):
           listIF=[]
           aseguraretorno=False

           for statement in self.statements:
             if isinstance(statement,Def_Fun):
                return False #Error ,No puede definir una funcion dentro de una funcion
             elif isinstance(statement,RiderNode) or isinstance(statement,MotorcicleNode):                 
                 return False #Error ,No puede definir un tipo especial dentro de una funcion
             elif isinstance(statement,ReturnNode) and  (statement.type=="continue"or statement.type=="break"):
                 return False #Error ,Esta declaracion no es valida dentro de una funcion    
             else:
                 
                if isinstance(statement,ReturnNode):
                 
                 validationstatement=statement.validate(context)
                 if not isinstance(validationstatement,bool):
                       return validationstatement
                 else:
                     aseguraretorno=True
                else :
                     
                      if isinstance(statement,IfCond):
                          listIF.append(statement)
                      validationstatement=statement.validate(context)
                      if not isinstance(validationstatement,bool):
                        return validationstatement

           for dec_if in listIF:
              if verificatealwaysReturn(dec_if):
                  aseguraretorno=True
           
           if normaliza(self.padre.typefun)!="void":

               if aseguraretorno:
                 return aseguraretorno #No se asegura que se retorne  , Error
               else:
                  return IncorrectCallError(" Not all code paths return a value	","",self.token.line,self.token.column)

        else:

             if self.padre is None:
              for statement in self.statements:
               
                if isinstance(statement,ReturnNode) :
                      return False #Error ,Esta declaracion no es valida 
                validationstatement=statement.validate(context)
                if not isinstance(validationstatement,bool):
                     return validationstatement
                
             else: 
                  for statement in self.statements:
                    
                   if isinstance(statement,Def_Fun):
                         return False #Error ,No puede definir una funcion en este ambito
                   elif isinstance(statement,RiderNode) or isinstance(statement,MotorcicleNode):                 
                        return False #Error ,No puede definir un tipo especial en este ambito
                   elif isinstance(statement,ReturnNode):
                       if (statement.type=="continue"or statement.type=="break") and context.enwhile==None:
                           return IncorrectCallError("This token is incorrect, it is not within a while scope","",self.token.line,self.token.column)
                   
                   validationstatement=statement.validate(context)
                   if not isinstance(validationstatement,bool):
                      return validationstatement
        return True
    
    def checktype(self,context:Context):                   
           for statement in self.statements:                    
               checktypeStatement=statement.checktype(context)
               if isinstance(checktypeStatement,CheckTypesError) :
                 return checktypeStatement
           return True
        

    def eval(self,context:Context):
      
         for statement in self.statements:     

          if not isinstance(statement,Def_Fun) and not isinstance(statement,RiderNode) and not isinstance(statement,MotorcicleNode) : 
              
           if not isinstance(statement,ReturnNode):       
                 evaluation=statement.eval(context)
                 if isinstance(evaluation,RuntimeError):
                    return evaluation
                 if evaluation!=None:
                    if evaluation=="break"or evaluation=="continue":
                           return evaluation
                    elif evaluation!="Nothing":
                        return evaluation
                    else:
                      if isinstance(self.padre,Def_Fun):                  
                        return 
                      else:
                          return "Nothing"
                       

           elif statement.type=="break":
                   return "break"
           elif statement.type=="continue":                  
                  return "continue"
           else:
              if statement.expr!=None:
                return statement.expr.eval(context)
              else:
                if isinstance(self.padre,Def_Fun):
                    return
                else:
                    return "Nothing"

    @staticmethod
    def type() -> str:
        return "Program"
    statements= list()


class TypeSpecial(Statement):
    def __init__(self):  
     self.id=None
     self.padre=None
     self.funciones=[]
     self.nuevocontext:Context=None
     self.functionsOfRiders=["select_aceleration","select_action"]
     self.functionsOfMotorcicles=["select_configuration"]
     self.token=None

    def validate(self,context:Context):
       self.nuevocontext = context.crearnuevocontexto()  
       self.addvars()
       
       #Hay que agregarle las variables de las motos o los pilotos
       for function in self.funciones:
          
           if isinstance(self,MotorcicleNode):
              if self.functionsOfMotorcicles.count(function.idfun)!=0:
                 self.functionsOfMotorcicles.remove(function.idfun)
              else:
                  return IncorrectCallError("the method was already defined or it is not valid to define a method with this name in this context","",self.token.line,self.token.column)
           elif isinstance(self,RiderNode):
               if self.functionsOfRiders.count(function.idfun)!=0:
                   self.functionsOfRiders.remove(function.idfun)
               else:
                    return IncorrectCallError("the method was already defined or it is not valid to define a method with this name in this context","",self.token.line,self.token.column)
           validationfun=function.validate(self.nuevocontext)
           if not isinstance(validationfun,bool):
               return validationfun
         
       return True

    def checktype(self,context:Context):
        for function in self.funciones:
            if normaliza(self.nuevocontext.enfuncion.typefun)!="void" :
              return  CheckTypesError("error in the return value of the function","",self.token.line,self.token.column)
            
            checktypefunction=function.checktype(context)
            if isinstance(checktypefunction,CheckTypesError):
               return checktypefunction

        return True

    def addvars(self):
        if isinstance(self,RiderNode):
            listvar=self.varsforRiders
        else:
            listvar=self.varsforBikes

        for var in listvar:
             assign=D_Assign()
             assign.id=var[0]
             assign.expr=var[2]
             assign.typevar=var[1]
             self.nuevocontext.define_var(var[0],assign,self.token)
        
    def refreshContext(self,dict):    
       keys=dict.keys()
       for key in keys:
            if self.nuevocontext.variables.keys().count(key)==1:
                self.nuevocontext.variables[key].expr=dict[key]
 

class MotorcicleNode(TypeSpecial):
   def __init__(self):  
     self.id=None
     self.padre=None
     self.funciones=[]
     self.nuevocontext:Context=None
     self.varsforBikes=[["brand",VariableType.STRING,"Honda"],["max_speed",VariableType.INT,0],["weight",VariableType.INT,0],["tires",VariableType.INT,5],["brakes",VariableType.INT,5],["chassis_stiffness",VariableType.INT,8],["acceleration",VariableType.INT,69.444],["probability_of_the_motorcycle_breaking_down",VariableType.DOUBLE,0.000001],["probability_of_exploding_tires",VariableType.DOUBLE,0.000001]]
     self.functionsOfMotorcicles=["select_configuration"]
     self.token=None

class RiderNode(TypeSpecial):
   def __init__(self):
     self.id=None
     self.padre=None
     self.funciones=[]
     self.nuevocontext:Context=None
     self.varsforRiders=[["speed",VariableType.DOUBLE,0],["aceleration",VariableType.DOUBLE,0],["time_lap",VariableType.DOUBLE,0]]
     self.functionsOfRiders=["select_aceleration","select_action"]
     self.token=None


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
        return self.ast.validate(context)
          

    def eval(self,context :Context):
       return self.ast.eval(context)


class Expression(Node):
    def __init__(self):
         self.nododreconocimiento= NodeE()
         self.noderaiz=NodeE()
         self.noderaiz=self.nododreconocimiento

    def checktype(self,context:Context):
        return self.noderaiz.checktype(context)

    def validate(self,context:Context):
        return self.noderaiz.validate(context)
            

    def eval(self,context:Context):
        return self.noderaiz.eval(context)

class D_Assign(Statement):
    def __init__(self):
       self.typevar: VariableType=None
       self.id : str
       self.expr : Expression=None
       self.isarray: bool=False
       self.arrayvalue:list()=[]
       self.token=None
    
    def validate(self, context: Context) -> bool: #@@
       if not self.isarray:
        
        validationexpr=self.expr.validate(context)
        if not isinstance(validationexpr,bool):
            validationexpr.line=self.token.line
            validationexpr.column=self.token.column
            return validationexpr        
        
        validationvar=context.define_var(self.id,self,self.token)
        if not isinstance(validationvar,bool):
            return validationvar

       else :
           for expresion in self.arrayvalue:
              if not expresion.validate(context):
                 return False
       return True

    def checktype(self,context:Context):
        if not self.isarray:
            typeExpression=self.expr.checktype(context)
            type= normaliza(self.typevar)
            if isinstance(typeExpression,CheckTypesError):           
                typeExpression.line=self.token.line
                typeExpression.column=self.token.column
                return typeExpression
            if typeExpression==type:
                return True
            return CheckTypesError("the induced type of the expression is different from the type of the variable","",self.token.line,self.token.column)
        else:
            for expression in arrayvalue:
                typeExpression=expression.checktype(context)
                if typeExpression!=typevar:
                 return False
            return True

    def eval(self,context:Context):
      return context.evalAttribute(self.id)
    

    @staticmethod
    def type() -> str:
        return "DecAssign"

class ReturnNode(Statement): 
    def __init__(self):
      self.type=""
      self.expr:Expression= Expression()
      self.padre=None
      self.token=None

    def validate(self,context:Context):
            
     if self.type=="continue"or self.type=="break":
         return True

     if context.enfuncion==None:
         return IncorrectCallError("You can not return pq is not within the scope of a function","",self.token.line,self.token.column)
        
     elif normaliza(context.enfuncion.typefun)=="void":
            if self.expr.noderaiz.ast!=None:
                return IncorrectCallError("The function does not expect to return an expression","",self.token.line,self.token.column)
                
     else:  
         if self.expr.noderaiz.ast==None:                
                return IncorrectCallError("An expression must be returned to the function","",self.token.line,self.token.column)

         validationexpr=self.expr.validate(context)
         if not isinstance(validationexpr,bool):
             validationexpr.line=self.token.line
             validationexpr.column=self.token.column
             return validationexpr
     
     return True

    def checktype(self,context:Context):
       if self.type=="continue"or self.type=="break":
         return True
       
       elif normaliza(context.enfuncion.typefun)!="void":
              checkexpr=self.expr.checktype(context)
              if isinstance(checkexpr,CheckTypesError):
                  checkexpr.line=self.token.line
                  checkexpr.column=self.token.column
                  return checkexpr
              if normaliza(context.enfuncion.typefun)==checkexpr:
                  return True
              else:
                 return CheckTypesError("the type of the expression does not correspond to the type that the method should return","",self.token.line,self.token.column)
       
       return True

class Redefinition(Statement):
     def __init__(self):
       self.id=None
       self.op=None
       self.expr:Expression=None
       self.token=None

     def validate(self, context: Context) -> bool:
         validationexpr=self.expr.validate(context)
         if not isinstance(validationexpr,bool):
             validationexpr.line=self.token.line
             validationexpr.column=self.token.column
             return validationexpr 
         
         return context.check_var(self.id,self.token)
              
         
         

     def checktype(self,context:Context):
          return self.op.checktype(context)         
     
     def eval(self,context:Context):
         evaloper=self.op.eval(context)
         if isinstance(evaloper,RuntimeError):
             return evaloper
         context.variables[self.id].value=evaloper

     @staticmethod
     def type() -> str:
        return "Redef"


class Def_Fun(Statement):
    def __init__(self):
      self.typefun:MethodType=None
      self.idfun: str=None
      self.args:list(list())=[]
      self.body:Program=None
      self.nuevocontext:Context=None
      self.token=None 

    def validate(self, context : Context) -> bool:
        if not isinstance(self.padre,RiderNode) and not isinstance(self.padre,MotorcicleNode):
           self.nuevocontext = context.crearnuevocontexto()
        else:
            self.nuevocontext=context

        validationfun=context.define_fun(self.idfun,self,self.token)
        if not isinstance(validationfun,bool):
            return validationfun

        for arg in self.args:
           var= D_Assign()
           var.typevar=arg[0]
           var.token=self.token
           validationArgs=self.nuevocontext.define_var(arg[1],var,self.token)
           if not isinstance(validationArgs,bool):
               return validationArgs

        self.nuevocontext.enfuncion=self
        validationbody=self.body.validate(self.nuevocontext)
        if not isinstance(validationbody,bool):
            return validationbody

        return True

        

        

    def checktype(self,context:Context):  
        return self.body.checktype(self.nuevocontext)

    def eval(self,args,context:Context):
      keys=list(self.nuevocontext.variables.keys())
      index=0
      for arg in args:
          evalexpression=arg.eval(context)
          if not isinstance(evalexpression,RuntimeError):
             self.nuevocontext.variables[keys[index]].value=evalexpression
             index+=1
          else:
              return evalexpression
      return self.body.eval(self.nuevocontext)

    @staticmethod
    def type() -> str:
        return "DefFun"

class Condition(Node):
     def __init__(self):
       self.expression1=Expression()
       self.expression2=Expression()
       self.comparador:Rel=None
       self.token=None

     def validate (self,context:Context):
         validationExpr1=self.expression1.validate(context)
         if isinstance(validationExpr1,IncorrectCallError):
             return validationExpr1
         if self.expression2.nododreconocimiento.ast != None:
          validationExpr2=self.expression2.validate(context)
          if isinstance(validationExpr2,IncorrectCallError):
             return validationExpr2
         return True

     def checktype(self,context:Context):
        
        checkExpr1=self.expression1.checktype(context)

        if self.expression2.nododreconocimiento.ast==None:
            if isinstance(checkExpr1,CheckTypesError):
                return checkExpr1
            else : return True

        else: 
              checktypecomp=self.comparador.checktype(context)
              if isinstance(checktypecomp,CheckTypesError):
                  if checktypecomp.line=="":
                     checktypecomp.line=self.token.line
                     checktypecomp.column=self.token.column
                  return checktypecomp
              else:
                  return True
              #checkExpr2=self.expression2.checktype(context)
              #if isinstance(checkExpr2,CheckTypesError):
               # return checkExpr2
              #if checkExpr1==checkExpr2:
               #    return True
              #else:
               #  return IncorrectCallError("Cannot compare two expressions with different types","","","")

     def eval(self,context:Context):
         return self.comparador.eval(context)

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
        
        for condition in self.conditions:
            validationCondition= condition.validate(context)
            if not isinstance(validationCondition,bool):
                 return validationCondition

       
        validationbody=self.body.validate(context)
        if not isinstance(validationbody,bool):
            return validationbody

        if self.nodoelse!=None:
             validationbodyelse=self.nodoelse.validate(context)
             if not isinstance(validationbodyelse,bool):
                return validationbodyelse
          
        return True

    def checktype(self,context:Context):
        for condition in self.conditions:
            checktypeCondition=condition.checktype(context)
            if isinstance(checktypeCondition,CheckTypesError) :
                return checktypeCondition
        
        checktypeBody=self.body.checktype(context)
        if isinstance(checktypeBody,CheckTypesError):
            return checktypeBody
        
        if self.nodoelse!=None:
          checktypeNodoelse=self.nodoelse.checktype(context)
          if isinstance(checktypeNodoelse,CheckTypesError) :
            return checktypeNodoelse

        
        return True

    def eval(self,context:Context):
        resultvalue:bool=None
        resultante=self.conditions[0].eval(context)
        if isinstance(resultante,RuntimeError):
            return resultante
        index=1

        while index<len(self.conditions):
               self.operadoresbinarios[index-1].left_node=resultante
               evalcond=self.conditions[index].eval(context)
               if isinstance(evalcond,RuntimeError):
                  return evalcond
               self.operadoresbinarios[index-1].right_node=evalcond
               resultante=self.operadoresbinarios[index-1].eval(context)
               index+=1                              

        if resultante:
          return self.body.eval(context)
        elif self.nodoelse!=None:
               return self.nodoelse.eval(context)

    @staticmethod
    def type() -> str:
        return "If"

class WhileCond(Statement):
    def __init__(self):
        self.operadoresbinarios=[]
        self.conditions:list(Condition)=[]
        self.body=Program()
        

    def validate (self,context:Context):
              
        for condition in self.conditions:
            validationcondition= condition.validate(context)
            if not isinstance(validationcondition,bool):
                 return validationcondition
             
        context.enwhile=self

        validationbody= self.body.validate(context)
        if not isinstance(validationbody,bool):
            return validationbody

        context.enwhile=None

        return True


    def checktype(self,context:Context):
        for condition in self.conditions:
            checktypeCondition=condition.checktype(context)
            if isinstance(checktypeCondition,CheckTypesError) :
                return checktypeCondition

        checktypeBody=self.body.checktype(context)
        if isinstance(checktypeBody,CheckTypesError):
            return checktypeBody
        return True

    def eval(self,context:Context):
        resultvalue:bool=None
        resultante=self.conditions[0].eval(context)
        if isinstance(resultante,RuntimeError):
            return resultante
        index=1

        while index<len(self.conditions):
               self.operadoresbinarios[index-1].left_node=resultante
               evalexpr= self.conditions[index].eval(context)
               if isinstance(evalexpr,RuntimeError):
                   return evalexpr
               self.operadoresbinarios[index-1].right_node=evalexpr
               resultante=self.operadoresbinarios[index-1].eval(context)
               index+=1                              

        if resultante:
            retorno=self.body.eval(context)
            if retorno =="continue" or retorno==None:
              return self.eval(context)
            elif not isinstance(retorno,str):
                  return retorno
        

    @staticmethod
    def type() -> str:
        return "While"

         


class NodeB(Node):
   def __init__(self):
    self.padre = None
    self.hijos= list()  
    self.ast = None 
   
   def refreshAST(self):
    if len(self.hijos)==2:
        if isinstance(self.padre,NodeE):
          self.ast=self.hijos[1].ast
        else:
            self.ast=self.padre.hijos[0]
            self.ast.right_node=self.hijos[1].ast
            if isinstance(self.padre.padre, NodeE):
                self.ast.left_node= self.padre.padre.hijos[0].ast
            else:
                self.ast.left_node= self.padre.padre.hijos[1].ast

class NodeX(Node):
    def __init__(self):
     self.padre = None
     self.hijos= list()
     self.ast=None

    def refreshAST(self):
     if len(self.hijos)==3:
           self.ast=self.hijos[2].ast
    
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
    self.aux=None

   def refreshAST(self):
    if len(self.hijos)==3:
        self.aux=self.hijos[1].ast
    elif len(self.hijos)==1:
         self.aux= self.hijos[0].ast
    else :
        self.ast=None
    
    if self.aux is not None:
        if isinstance(self.padre,NodeB):
            self.ast=self.aux
        else:
            self.ast= self.padre.hijos[0]
            self.ast.right_node=self.aux
            if isinstance(self.padre.padre, NodeB):
                self.ast.left_node=self.padre.padre.hijos[0].ast
            else:
                self.ast.left_node=self.padre.padre.hijos[1].ast
                  
class NodeY:  
    def __init__(self):
     self.ast=None
     self.padre= None
     self.hijos= list()

    def refreshAST(self):
     if len(self.hijos)==3:
       self.ast=self.hijos[2].ast
    
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

class Val(Node):#@@
    def __init__(self,val):
     self.val=val
     self.type=None

    def validate(self,context:Context):
        return True

    def checktype (self,context:Context): 
        if self.val.token_type==TokenType.T_I_VALUE:
            self.type=9
            return "int"
        if self.val.token_type==TokenType.T_D_VALUE:
            self.type= 4.5
            return "double"

        if self.val.token_type==TokenType.T_FALSE or self.val.token_type==TokenType.T_TRUE:
            if self.val.token_type==TokenType.T_FALSE:
                self.type=False
            else:
                self.type=True
            return "bool"
        if self.val.token_type==TokenType.T_S_VALUE:
            self.type="DD"
            return "str"
       
    def eval(self,context:Context):
        if self.type==True or self.type==False:
            return self.type
        else:
             return ((type(self.type))(self.val.value))
        

    @staticmethod
    def type() -> str:
        return "EXP"

class Variable(Node):
    def __init__(self,token:Token):
        self.idvar= token.value
        self.token=token

    def validate(self,context:Context): 
        return context.check_var(self.idvar,self.token)

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

    def eval(self,context:Context):
        return context.getvalueAttribute(self.idvar,self.token)


    @staticmethod
    def type() -> str:
        return "Variable"



class FunCall(Node):  
    def __init__(self):  
     self.id: str is None
     self.args:list()=[]
     self.token=None

    def validate (self,context:Context)->bool: 
       for expr in self.args:
           validationexpr=expr.validate(context)
           if not isinstance(validationexpr,bool):
               validationexpr.line= self.token.line
               validationexpr.column= self.token.column
               return validationexpr

       return context.check_fun(self.id,len(self.args),self.token)

    def checktype (self,context:Context):   
        index=0 
        definitionfuncion =context.getFunction(self.id)
        keys= list(definitionfuncion.nuevocontext.variables.keys())

        for arg in self.args:
          typeExp=arg.checktype(context)
          if isinstance(typeExp,CheckTypesError):
              return typeExp
          if typeExp!=normaliza(definitionfuncion.nuevocontext.variables[keys[index]].typevar):
              return CheckTypesError("the parameter entered is not of the expected type","",self.token.line,self.token.column)##Anadir error (el parametro ingresado no es del tipo esperado)
          index+=1

        type=context.gettypefun(self.id)
        if type==MethodType.INT:
          return "int"
        if type==MethodType.BOOL:
          return "bool"
        if type==MethodType.DOUBLE:
          return "double"
        if type==MethodType.STRING:
          return "str"

    def eval(self,context:Context):
        return context.getFunction(self.id).eval(self.args,context)



    @staticmethod
    def type() -> str:
        return "FunCall"  