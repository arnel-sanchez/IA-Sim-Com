    def CreaNododAsignacion(self,termino):
        if termino=="E" :
            nodonuevo= Expresion()
            nodonuevo.Padre=self.nodoactual
            self.nodoactual.Statments.append(nodonuevo)
            self.nodoactual=nodonuevo
            self.estadoAST=EstadoDAST.EnExpresion
        elif termino==TokenType.T_INT :
            nodonuevo= IntInit()
        elif termino==TokenType.T_BOOL :
            nodonuevo= BoolInit()
        elif termino==TokenType.T_DOUBLE :
            nodonuevo= DoubleInit()
        elif termino==TokenType.T_ID :
            nodonuevo= Id()
        elif termino==TokenType.T_ASSIGN :
            nodonuevo= Assign()
        elif termino==TokenType.T_STRING:
            nodonuevo= StringInit()
        elif termino==TokenType.T_ARRAY:
            nodonuevo= ArrayInit()
        self.nodoactual.Statments.append(nodonuevo)

    def CreaNododExpresion(self,termino):
        #Falta Implementarlo
        return 3

    def CreaNododProgram(self,termino):
        if termino=="D":
            nuevonodo = D_Assign()
            self.nodoactual.statments.append(nuevonodo)
            self.nodoactual=nuevonodo
            self.estadoDAST=EstadoDAST.EnAsignacion
        elif termino==TokenType.T_METHOD:
            nuevonodo= Def_Fun()
            self.nodoactual.statments.append(nuevonodo)
            self.nodoactual=nodonuevo
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
            self.estadoDAST=EstadoDAST.EnIf
        elif termino == TokenType.T_WHILE :
            nuevonodo = WhileCond()
            self.nodoactual.statments.append(nuevonodo)
            self.nodoactual=nodonuevo
            self.estadoDAST=EstadoDAST.EnWhile
            
    def parse(self, lines: [[Token]]) -> Error:
        for line in lines:
            self.parsear(line, 0, "L")
        return self.error
    

    def EligeTipoDdeclaracion(self,termino):
        if self.estadoDAST==EstadoDAST.EnAsignacion:
            self.CreaNododAsignacion(termino)
        elif self.estadoDAST==EstadoDAST.EnProgram:
            self.CreaNododProgram(termino)
        elif self.estadoDAST==EstadoDAST.EnIf:
            self.CreaNododIf(termino)
