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


def parsear(self, line, i, cadena):
        self.error = None
        estados = []  # Aqui guardamos los estados en forma de string , de forma que si el ultimo estado de la lista es el estado en el que estoy y si no hay estados en la lista ent estamos fuera de cualquier ambito del programa
        for termino in cadena:
            if i < len(line):
                if i == 0:
                    if len(estados) != 0:
                        estado = estados[- 1]
                        if estado == Region.R_TYPE:
                            if line[i].token_type != (TokenType.T_METHOD and TokenType.T_CLOSE_BRACE):
                                self.error = Error("Error", "", "", 0, 0)#
                                break
                        elif estado == Region.R_IF or estado == Region.R_ELIF or estado == Region.R_ELSE:
                            if line[i].token_type == (TokenType.T_METHOD or TokenType.T_RETURN or TokenType.T_BREAK or
                                                      TokenType.T_CONTINUE or TokenType.T_MOTORCYCLE or
                                                      TokenType.T_RIDER):
                                self.error = Error("Error", "", "", 0, 0)#
                                break
                        elif estado == Region.R_WHILE:
                            if line[i].token_type == (TokenType.T_METHOD or TokenType.T_RETURN or
                                                      TokenType.T_MOTORCYCLE or TokenType.T_RIDER):
                                self.error = Error("Error", "", "", 0, 0)#
                                break
                if termino == line[i].token_type:
                    if line[i].token_type == (TokenType.T_RIDER or TokenType.T_MOTORCYCLE):
                        estados.append(Region.R_TYPE)
                    elif line[i].token_type == TokenType.T_METHOD:
                        estados.append(Region.R_METHOD)
                        self.context=self.context.creanuevocontexto()
                    elif line[i].token_type == TokenType.T_WHILE:
                        estados.append(Region.R_WHILE)
                        self.context=self.context.creanuevocontexto()
                    elif line[i].token_type == TokenType.T_IF:
                        estados.append(Region.R_IF)
                        self.context=self.context.creanuevocontexto()
                    elif line[i].token_type == TokenType.T_ELIF:
                        self.context=self.context.creanuevocontexto()
                        if estados[- 1] == (Region.R_IF or Region.R_ELIF):
                            estados.pop()
                            estados.append(Region.R_ELIF)
                        else:
                            self.error = Error("", "", "", 0, 0)#
                            break
                    elif line[i].token_type == TokenType.T_ELSE:
                        self.context=self.context.creanuevocontexto()
                        if estados[- 1] == (Region.R_IF or Region.R_ELIF):
                            estados.pop()
                            estados.append(Region.R_ELSE)
                        else:
                            self.error = Error("", "", "", 0, 0)#
                            break
                    elif line[i].token_type == TokenType.T_CLOSE_BRACE:
                        self.context= self.context.contextoPadre
                        if i + 1 == len(line) or estados[- 1] != (Region.R_IF and Region.R_ELIF):
                            estados.pop()
                    i += 1
                    continue
                elif isinstance(termino, TokenType):
                    self.error = Error("", "", "", 0, 0)#
                    break
                indice_nt = self.no_terminales.index(termino)
                indice_t = self.terminales.index(line[i].token_type)
                if self.matriz[indice_nt][indice_t] != (None and "e"):
                    self.parsear(line, i, self.matriz[indice_nt][indice_t])
                    if self.error is not None:
                        break
                elif self.matriz[indice_nt][indice_t] != "e":
                    self.error = Error("", "", "", 0, 0)#Aqui debemos agregar el error , con ello la linea y la columna que fue para posteriormente comunicarselo al usuario
                    break
            else:
                break
