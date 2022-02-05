from compilation.ast.nodes import *
from compilation.enums import VariableType
from compilation.ast.complex import Expression, normaliza
from compilation.context import Context


def is_string(value: str) -> bool:
    return isinstance(value, str)

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

class Assign(Node):
    def __init__(self, idnode: Node):
        self.idnode = idnode
        self.expression:Expression = None
        self.token=None

    def checktype(self,context:Context):
        
        checkexpr=self.expression.checktype(context)
        if isinstance(checkexpr,CheckTypesError):            
            checkexpr.line=self.token.line
            checkexpr.column=self.token.column
            return checkexpr

        if checkexpr==normaliza(context.gettypevar(self.idnode)):
            return True
        else :
           return CheckTypesError("the expression to be assigned is not of the same type as the variable","",self.token.line,self.token.column)

    def eval(self,context:Context):
       return self.expression.eval(context)
        

    @staticmethod
    def review(variables: dict, var_id: str, value):
        variables[var_id] = value
        return value

    def __repr__(self):
        return "{}_ASSIGN({}, {})".format(self.type(), self.id_node, self.expression)

    @staticmethod
    def type() -> str:
        return "U"

class OpAs(Assign):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None
        self.token=None
    
    def checktype(self,context:Context):
        
        checkexpr=self.expression.checktype(context)
        if isinstance(checkexpr,CheckTypesError):
            checkexpr.line=self.token.line
            checkexpr.column=self.token.column
            return checkexpr

        if normaliza(context.gettypevar(self.idnode))=="int":
            if checkexpr=="int":
                return True
            else:
                return CheckTypesError("the induced type of the expression is different from the type of the variable","",self.token.line,self.token.column)
        elif normaliza(context.gettypevar(self.idnode))=="double":
            if checkexpr=="int" or checkexpr=="double":
                return True
            else:
                return CheckTypesError("The induced type of the expression is not a number","",self.token.line,self.token.column)
        else:
            return CheckTypesError("It is incorrect to apply this operation on this type of variables","",self.token.line,self.token.column)

    def __repr__(self):
        return "{}_AS({}, {})".format(self.type(), self.id_node, self.expression)

    @staticmethod
    def type() -> str:
        return "OP"

class AddAs(OpAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None
        self.token=None

    def eval(self,context:Context):
        if context.variables[self.idnode].value==None:
           return RuntimeError("local variable {} referenced before assignment".format(self.id_node),"",self.token.line,self.token.column)
        evalexpression=self.expression.eval(context)
        if isinstance(evalexpression,RuntimeError):
            return evalexpression
        if context.variables[self.idnode].typevar==VariableType.INT:
          return (int)(context.variables[self.idnode].value + evalexpression)
        else:
            return (float)(context.variables[self.idnode].value + evalexpression)
   
    def type() -> str:
        return "ADD"


class ArAs(OpAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    def review(self, variables: dict, var_id: str, value):
        if not is_number(variables[var_id]):
            return Error("Error", "", "", 0, 0)  #
        if not is_number(value):
            return Error("Error", "", "", 0, 0)  #
        return self.operation(variables, var_id, value)

    @staticmethod
    def operation(variables: dict, var_id: str, value):
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "AR"


class SubAs(ArAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None
        self.token=None



    def eval(self,context:Context):
        if context.variables[self.idnode].value==None:
           return RuntimeError("local variable {} referenced before assignment".format(self.id_node),"",self.token.line,self.token.column)
        evalexpression=self.expression.eval(context)
        if isinstance(evalexpression,RuntimeError):
            return evalexpression
        if context.variables[self.idnode].typevar==VariableType.INT:
          return (int)(context.variables[self.idnode].value - evalexpression)
        else:
            return (float)(context.variables[self.idnode].value - evalexpression)

    @staticmethod
    def type() -> str:
        return "SUB"


class MulAs(OpAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None
        self.token=None
    
    def eval(self,context:Context):
        if context.variables[self.idnode].value==None:
           return RuntimeError("local variable {} referenced before assignment".format(self.id_node),"",self.token.line,self.token.column)
        evalexpression=self.expression.eval(context)
        if isinstance(evalexpression,RuntimeError):
            return evalexpression
        if context.variables[self.idnode].typevar==VariableType.INT:
          return (int)(context.variables[self.idnode].value * evalexpression)
        else:
            return (float)(context.variables[self.idnode].value * evalexpression)

    @staticmethod
    def type() -> str:
        return "MUL"


class DivAs(ArAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None
        self.token=None

   
    def eval(self,context:Context):
          if context.variables[self.idnode].value==None:
           return RuntimeError("local variable {} referenced before assignment".format(self.id_node),"",self.token.line,self.token.column)
          nododDivision=self.expression.eval(context)
          if isinstance(nododDivision,RuntimeError):
              return nododDivision
          
          if nododDivision==0:
              return  RuntimeError("division by zero","",self.token.line,self.token.column)
          elif context.variables[self.idnode].typevar==VariableType.INT: 
                return (int)(context.variables[self.idnode].value / nododDivision)
          else:
              return (float)(context.variables[self.idnode].value / nododDivision)

             
          

    @staticmethod
    def type() -> str:
        return "DIV"


class ModAs(DivAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None
        self.token=None

    def eval(self,context:Context):
          if context.variables[self.idnode].value==None:
           return RuntimeError("local variable {} referenced before assignment".format(self.id_node),"",self.token.line,self.token.column)
          nododDivision=self.expression.eval(context)
          if isinstance(nododDivision,RuntimeError):
              return nododDivision
          
          if nododDivision==0:
              return  RuntimeError("division by zero","",self.token.line,self.token.column)
          elif context.variables[self.idnode].typevar==VariableType.INT: 
                return (int)(context.variables[self.idnode].value % nododDivision)
          else:
              return (float)(context.variables[self.idnode].value % nododDivision)



    @staticmethod
    def type() -> str:
        return "MOD"


class ExpAs(ArAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None
        self.token=None


    def checktype(self,context:Context):
        
        checkexpr=self.expression.checktype(context)
        if isinstance(checkexpr,CheckTypesError):
            checkexpr.line=self.token.line
            checkexpr.column=self.token.column
            return checkexpr

        if normaliza(context.gettypevar(self.idnode))=="int" or normaliza(context.gettypevar(self.idnode))=="double":
              if checkexpr=="int":
                  return True
              else:
                  return CheckTypesError("the exponent must be an integer","",self.token.line,self.token.column)
        else:
            return CheckTypesError("incorrect variable type for power operation","",self.token.line,self.token.column)

    
    def eval(self,context:Context):
          
          if context.variables[self.idnode].value==None:
            return RuntimeError("local variable {} referenced before assignment".format(self.id_node),"",self.token.line,self.token.column)
          exponente=self.expression.eval(context)
          if isinstance(exponente,RuntimeError):
            return exponente

          if context.variables[self.idnode].typevar==VariableType.INT: 
              return (int)(context.variables[self.idnode].value ** exponente)
          else:
              return (float)(context.variables[self.idnode].value ** exponente)

    @staticmethod
    def type() -> str:
        return "EXP"


class BoolAs(OpAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None
        self.token=None

    def checktype(self,context:Context):
        
        checkexpr=self.expression.checktype(context)
        if isinstance(checkexpr,CheckTypesError):
            checkexpr.line=self.token.line
            checkexpr.column=self.token.column
            return checkexpr

        if checkexpr==normaliza(context.gettypevar(self.idnode)):
            return True
        else :
            return CheckTypesError("the expression to be assigned is not of the same type as the variable","",self.token.line,self.token.column)


    @staticmethod
    def type() -> str:
        return "BOOL"


class AndAs(BoolAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None
        self.token=None
    
    def eval(self,context:Context):
        
        if context.variables[self.idnode].value==None:
           return RuntimeError("local variable {} referenced before assignment".format(self.id_node),"",self.token.line,self.token.column)
        evalexpression=self.expression.eval(context)
        if isinstance(evalexpression,RuntimeError):
            return evalexpression
        
        return context.variables[self.idnode].value & evalexpression 

    @staticmethod
    def type() -> str:
        return "AND"


class OrAs(BoolAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None
        self.token=None

    def eval(self,context:Context):
        
        if context.variables[self.idnode].value==None:
           return RuntimeError("local variable {} referenced before assignment".format(self.id_node),"",self.token.line,self.token.column)
        evalexpression=self.expression.eval(context)
        if isinstance(evalexpression,RuntimeError):
            return evalexpression
        
        return context.variables[self.idnode].value | evalexpression 

    @staticmethod
    def type() -> str:
        return "OR"


class XorAs(BoolAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None
        self.token=None
    
    def eval(self,context:Context):
        
        if context.variables[self.idnode].value==None:
           return RuntimeError("local variable {} referenced before assignment".format(self.id_node),"",self.token.line,self.token.column)
        evalexpression=self.expression.eval(context)
        if isinstance(evalexpression,RuntimeError):
            return evalexpression
        
        return context.variables[self.idnode].value ^ evalexpression 

    @staticmethod
    def type() -> str:
        return "XOR"
