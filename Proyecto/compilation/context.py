from compilation.enums import *

class Context:    
    def __init__(self):
     self.variables=dict()
     self.funciones=dict()
     self.errors=list()
     self.contextPadre = None 

    def gettypefun(self,idfun):
       Esta= self.funciones.get(idfun,"NoEsta")
       if Esta!="NoEsta":
           return self.funciones[idfun][0]
       else:
           context = self.contextPadre
           while context is not None:
                 funContain = context.funciones.get(idfun,"NoEsta")
                 if funContain != "NoEsta":
                     return context.funciones[idfun][0]
                 context=context.contextPadre


    def gettypevar(self,idvar:str):
       Esta= self.variables.get(idvar,"NoEsta")
       if Esta !="NoEsta":
           return self.variables[idvar]
       else:
           context = self.contextPadre
           while context is not None:
                 varContain = context.variables.get(idvar,"NoEsta")
                 if varContain != "NoEsta":
                     return context.variables[idvar]
                 context=context.contextPadre


    def check_var(self,var:str)->bool :
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
             return False

    def check_fun(self,fun:str,args:int)->bool :
         funContain = self.funciones.get(fun,"NoEsta")
         if funContain != "NoEsta" and args==funContain:
             return True
         else :
             context = self.contextPadre
             while context is not None:
                 funContain = context.funciones.get(fun,"NoEsta")
                 if funContain != "NoEsta" and args==funContain:
                     return True
                 context=context.contextPadre
             return False

    def define_fun(self,fun:str,type:MethodType,args:list)->bool :
        funContain = self.funciones.get(fun,"NoEsta")
        if funContain != "NoEsta":
            self.errors.append("ya existe una funcion con este nombre en este contexto")
            return False
        else:
            self.funciones.setdefault(fun,[type,len(args)])
        return True

    def define_var(self,var:str,type:VariableType)->bool :
        varContain = self.variables.get(var,"NoEsta")
        if varContain != "NoEsta":
            self.errors.append("ya existe una variable con este nombre en este contexto")
            return False
        else:
            self.variables.setdefault(var,type)
        return True

    def crearnuevocontexto(self) :
          nuevocontext=Context()
          nuevocontext.contextPadre=self
          return nuevocontext
