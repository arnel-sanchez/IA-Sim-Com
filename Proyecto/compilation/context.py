from compilation.errors import IncorrectCallError
from compilation.tokens import*
from compilation.enums import *

class Context:    
    def __init__(self):
     self.variables=dict()
     self.funciones=dict()
     self.errors=list()
     self.contextPadre = None 
     self.enfuncion=None
     self.enwhile=None

    def evalAttribute(self,idvar):
        self.variables[idvar].expr=self.variables[idvar].expr.noderaiz.eval(self)

    def getFunction(self,id):
         funContain = self.funciones.get(id,"NoEsta")
         if funContain != "NoEsta" :
             return funContain
         else :
             context=self.contextPadre
             while context is not None:
                 funContain = context.funciones.get(id,"NoEsta")
                 if funContain != "NoEsta":
                     return funContain
                 context=context.contextPadre
            
        

    def getvalueAttribute(self,var):
         if self.variables.get(var,"NoEsta")!="NoEsta":
              return self.variables[var].expr
         else:
             
             context=self.contextPadre
             while context!=None :
                  if context.variables.get(var,"NoEsta")!="NoEsta":
                    retorno = context.variables[var].expr
                    return retorno
                  context=context.padre
     
    def getvaluefunction(idfun,args):
         context=self
         if self.funciones.get(idfun,"NoEsta")!="NoEsta":
                funcion=self.funciones[idfun]
         else:
             context=self.padre
             while context!=null :
                  if context.funciones.get(var,"NoEsta")!="NoEsta":
                    funcion = context.funciones[idfun]
                    break
                  context=context.padre

         return funcion.eval(args,context)

         
    def gettypefun(self,idfun):
       Esta= self.funciones.get(idfun,"NoEsta")
       if Esta!="NoEsta":
           return self.funciones[idfun].typefun
       else:
           context = self.contextPadre
           while context is not None:
                 funContain = context.funciones.get(idfun,"NoEsta")
                 if funContain != "NoEsta":
                     return context.funciones[idfun].typefun
                 context=context.contextPadre


    def gettypevar(self,idvar:str):
       Esta= self.variables.get(idvar,"NoEsta")
       if Esta !="NoEsta":
           return self.variables[idvar].typevar
       else:
           context = self.contextPadre
           while context is not None:
                 varContain = context.variables.get(idvar,"NoEsta")
                 if varContain != "NoEsta":
                     return context.variables[idvar].typevar
                 context=context.contextPadre


    def check_var(self,var:str,token:Token):
         varContain = self.variables.get(var,"NoEsta")
         if varContain != "NoEsta":
             return True
         else :

             context=self.contextPadre
             while context is not None:
                 varContain = context.variables.get(var,"NoEsta")
                 if varContain != "NoEsta":
                     return True
                 context=context.contextPadre
             return IncorrectCallError("there is no variable with this name accessible from this scope","",token.line,token.column)

    def check_fun(self,fun:str,args:int,token:Token) :
         funContain = self.funciones.get(fun,"NoEsta")
         if funContain != "NoEsta" and args== len(funContain.args):
             return True
         else :
             context=self.contextPadre
             while context is not None:
                 funContain = context.funciones.get(fun,"NoEsta")
                 if funContain != "NoEsta" and args==len(funContain.args):
                     return True
                 context=context.contextPadre
             return IncorrectCallError("there is no function with this name accessible from this scope","",token.line,token.column)
    def define_fun(self,fun:str, node,token:Token):
        funContain = self.funciones.get(fun,"NoEsta")
        if funContain != "NoEsta":
            return IncorrectCallError("a function with this name already exists in this context","",token.line,token.column)
        else:
            self.funciones.setdefault(fun,node)
        return True
    def define_var(self,id:str,var,token:Token) :
        varContain = self.variables.get(id,"NoEsta")
        if varContain != "NoEsta":
            return IncorrectCallError("a variable with this name already exists in this context","",token.line,token.column)
        else:
            self.variables.setdefault(id,var)
        return True
    def crearnuevocontexto(self) :
          nuevocontext=Context()
          nuevocontext.contextPadre=self

          return nuevocontext
