

class Context:
    variables = dict()
    funciones=dict()
    errors=list()
    contextPadre = None 

    def gettypefun(self,idfun):
       Esta= self.funciones.get(idfun,"NoEsta")
       if Esta!="Noesta":
           return self.funciones[idfun][0]
       else:
           while self.contextPadre!=None:
                 context=self.contextPadre
                 funContain = context.funciones.get(idfun,"NoEsta")
                 if funContain != "NoEsta":
                     return context.funciones[idfun][0]

    def gettypevar(self,idvar:str):
       Esta= self.variables.get(idvar,"NoEsta")
       if Esta!="Noesta":
           return self.variables[idvar]
       else:
           while self.contextPadre!=None:
                 context=self.contextPadre
                 varContain = context.variables.get(idvar,"NoEsta")
                 if varContain != "NoEsta":
                     return context.variables[idvar]


    def check_var(self,var:str)->bool :
         varContain = self.variables.get(var,"NoEsta")
         if varContain != "NoEsta":
             return True
         else :
             while self.contextPadre!=None:
                 context=self.contextPadre
                 varContain = context.variables.get(var,"NoEsta")
                 if varContain != "NoEsta":
                     return True
             return False

    def check_fun(self,fun:str,args:int)->bool :
         funContain = self.funciones.get(fun,"NoEsta")
         if funContain != "NoEsta" and args==funContain:
             return True
         else :
             while self.contextPadre!=Null:
                 context=self.contextPadre
                 funContain = context.funciones.get(fun,"NoEsta")
                 if funContain != "NoEsta" and args==funContain:
                     return True
             return False
    def define_fun(self,fun:str,type:MethodType,args:list())->bool :
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
