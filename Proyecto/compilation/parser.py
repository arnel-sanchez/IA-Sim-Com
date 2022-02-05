from compilation.errors import *
from compilation.tokens import TokenType, Token
from compilation.enums import Region, EstadoDAST
from compilation.context import Context
from compilation.ast.assignments import *
from compilation.ast.auxiliary import *
from compilation.ast.complex import *
from compilation.ast.nodes import *
from compilation.ast.operations import *
from compilation.ast.relations import *


class Parser:
    def __init__(self):
        self.estados = []  # Aqui guardamos los estados en forma de string , de forma que si el ultimo estado de la lista es el estado en el que estoy y si no hay estados en la lista ent estamos fuera de cualquier ambito del programa
        self.context=Context()
        self.i=0
        self.Riders=[]
        self.Motorcicles=[]
        self.estadoDAST= EstadoDAST.EnProgram
        self.nodoactual=Program()  #Este sera el nodo en el que estoy parado cuando estoy construyendo el AST
        self.nodopararecorrerast=self.nodoactual
        self.producciones = {"L": [["D", TokenType.T_SEMICOLON], ["@"], [TokenType.T_CLOSE_BRACE, "N"],
                                   ["W", TokenType.T_SEMICOLON], [TokenType.T_METHOD, "R"],
                                   ["F", TokenType.T_ID, TokenType.T_OPEN_BRACE],[TokenType.T_ID,"H",TokenType.T_SEMICOLON]],
                             "D": [[TokenType.T_BOOL, TokenType.T_ID, TokenType.T_ASSIGN, "E"],
                                   [TokenType.T_INT, TokenType.T_ID, TokenType.T_ASSIGN, "E"],
                                   [TokenType.T_STRING, TokenType.T_ID, TokenType.T_ASSIGN, "E"],
                                   [TokenType.T_DOUBLE, TokenType.T_ID, TokenType.T_ASSIGN, "E"],
                                   [TokenType.T_ARRAY, "^"]],
                             "T": [[TokenType.T_STRING], [TokenType.T_INT], [TokenType.T_DOUBLE], [TokenType.T_BOOL]],
                             "R": [["K", TokenType.T_ID, TokenType.T_OPEN_PAREN, "P", TokenType.T_CLOSE_PAREN,
                                    TokenType.T_OPEN_BRACE]],
                             "K": [["T"], [TokenType.T_VOID]],
                             "P": [["T", TokenType.T_ID, "~"], ["e"]],
                             "~": [[TokenType.T_COMMA, "T", TokenType.T_ID, "~"], ["e"]],
                             "@": [[TokenType.T_IF, TokenType.T_OPEN_PAREN, "G", TokenType.T_CLOSE_PAREN,
                                    TokenType.T_OPEN_BRACE],
                                   [TokenType.T_WHILE, TokenType.T_OPEN_PAREN, "G", TokenType.T_CLOSE_PAREN,
                                    TokenType.T_OPEN_BRACE]],
                             "N": [[TokenType.T_ELSE, TokenType.T_OPEN_BRACE],
                                   [TokenType.T_ELIF, TokenType.T_OPEN_PAREN, "G", TokenType.T_CLOSE_PAREN,
                                    TokenType.T_OPEN_BRACE], ["e"]],
                             "W": [[TokenType.T_CONTINUE], [TokenType.T_BREAK], [TokenType.T_RETURN,"E"]],
                             "F": [[TokenType.T_RIDER], [TokenType.T_BIKE]],
                             "A": [[TokenType.T_OPEN_PAREN, "Z"
                                    , TokenType.T_CLOSE_PAREN], ["e"]],
                             "Z": [["e"],["E","U"]],
                             "I": [[TokenType.T_ASSIGN],[TokenType.T_ADD_AS], [TokenType.T_SUB_AS], [TokenType.T_DIV_AS],
                                   [TokenType.T_MUL_AS], [TokenType.T_MOD_AS], [TokenType.T_EXP_AS],[TokenType.T_AND_AS],[TokenType.T_OR_AS],[TokenType.T_XOR_AS]],
                             "Q": [[TokenType.T_S_VALUE],[TokenType.T_I_VALUE],[TokenType.T_D_VALUE],[TokenType.T_TRUE],[TokenType.T_FALSE],[TokenType.T_ID,"A"]],
                             "C": [[TokenType.T_GREQ_REL], [TokenType.T_GREAT_REL], [TokenType.T_LESS_REL],
                                   [TokenType.T_LEQ_REL],[TokenType.T_EQ_REL], [TokenType.T_NEQ_REL]],
                             "M": [["Q"], [TokenType.T_OPEN_PAREN, "E", TokenType.T_CLOSE_PAREN]],
                             "Y": [["e"], [TokenType.T_MUL_OP, "M", "Y"],[TokenType.T_DIV_OP, "M", "Y"],[TokenType.T_MOD_OP, "M", "Y"],[TokenType.T_EXP_OP, "M", "Y"]],
                             "J": [["e"], ["O", "S"]],
                             "U": [["e"], [TokenType.T_COMMA, "E", "U"]],
                             "X": [[TokenType.T_ADD_OP, "B","X"], [TokenType.T_SUB_OP,"B","X"],["e"]],
                             "E": [["B","X"]],
                             "B": [["M","Y"]],
                             "G": [["E","J"]],
                             "S": [["e"],[TokenType.T_OR_OP,"G"],[TokenType.T_AND_OP,"G"],[ TokenType.T_XOR_OP, "G"]],
                             "^": [["T", TokenType.T_ID, TokenType.T_ASSIGN, TokenType.T_OPEN_BRACKET,
                                    "E", "U", TokenType.T_CLOSE_BRACKET]],
                             "H": [[ "I","E"],[TokenType.T_OPEN_PAREN, "Z"
                                    ,TokenType.T_CLOSE_PAREN]],
                             "O": [[ "C","E"],["e"]]} 
                                  
        self.terminales = [TokenType.T_SEMICOLON, TokenType.T_OPEN_PAREN, TokenType.T_CLOSE_PAREN,
                           TokenType.T_OPEN_BRACKET, TokenType.T_CLOSE_BRACKET, TokenType.T_OPEN_BRACE,
                           TokenType.T_CLOSE_BRACE, TokenType.T_COMMENT, TokenType.T_STRING, TokenType.T_INT,
                           TokenType.T_DOUBLE, TokenType.T_BOOL, TokenType.T_TRUE, TokenType.T_FALSE, TokenType.T_IF,
                           TokenType.T_ELIF, TokenType.T_ELSE, TokenType.T_WHILE, TokenType.T_METHOD, TokenType.T_ID,
                           TokenType.T_ADD_OP, TokenType.T_SUB_OP, TokenType.T_NEG_OP, TokenType.T_MUL_OP,
                           TokenType.T_DIV_OP, TokenType.T_MOD_OP, TokenType.T_EXP_OP, TokenType.T_EQ_REL,
                           TokenType.T_NEQ_REL, TokenType.T_LESS_REL, TokenType.T_LEQ_REL, TokenType.T_GREAT_REL,
                           TokenType.T_GREQ_REL, TokenType.T_AND_OP, TokenType.T_OR_OP, TokenType.T_XOR_OP,
                           TokenType.T_ASSIGN, TokenType.T_ADD_AS, TokenType.T_SUB_AS, TokenType.T_MUL_AS,
                           TokenType.T_DIV_AS, TokenType.T_MOD_AS, TokenType.T_EXP_AS, TokenType.T_AND_AS,
                           TokenType.T_OR_AS, TokenType.T_XOR_AS, TokenType.T_DOT, TokenType.T_COMMA, TokenType.T_COLON,
                           TokenType.T_CARRIAGE, TokenType.T_NEWLINE, TokenType.T_INVALID, TokenType.T_S_VALUE,
                           TokenType.T_I_VALUE, TokenType.T_D_VALUE, TokenType.T_ARRAY, TokenType.T_VOID,
                           TokenType.T_CONTINUE, TokenType.T_BREAK, TokenType.T_RETURN, TokenType.T_RIDER,
                           TokenType.T_BIKE]
        self.no_terminales = ["L", "D", "I", "E", "M", "Y", "J", "U", "N", "@", "R", "K", "T", "P", "W", "S", "F",
                              "A", "Z", "Q", "C", "B", "G", "X", "~", "^","H","O"]
        self.first = dict()  # Guardamos los terminales que pertenecen al First de cada produccion posible de nuestra gramatica
        self.follow = {"L": [], "D": [], "I": [], "E": [], "M": [], "Y": [], "J": [], "U": [], "N": [], "@": [],
                       "R": [], "K": [], "T": [], "P": [], "W": [], "S": [], "F": [], "A": [], "Z": [],
                        "Q": [], "C": [], "B": [], "G": [], "X": [], "~": [],
                       "^": [],"H": [],"O":[]}
                                
        self.completafollow = {"L": [], "D": [], "I": [], "E": [], "M": [], "Y": [], "J": [], "U": [], "N": [], "@": [],
                       "R": [], "K": [], "T": [], "P": [], "W": [], "S": [], "F": [], "A": [], "Z": [],
                        "Q": [], "C": [], "B": [], "G": [], "X": [], "~": [],
                       "^": [], "H":[], "O" : []} 
                                    # Aqui guardamos los terminales que pertenecen al Follow de cada no terminal
        self.pendiente_follow = []  # Los elementos de esta lista tendran una forma "A,B" lo que significa que todo lo que pertenece al Follow de A tambien pertenece al Folow de B
        self.matriz = [[None for _ in range(len(self.terminales))] for _ in range(len(self.no_terminales))]
        self.lista_producciones = [["L", "D", TokenType.T_SEMICOLON], ["L", "@"], ["L", TokenType.T_CLOSE_BRACE, "N"],
                                   ["L", "W", TokenType.T_SEMICOLON], ["L", TokenType.T_METHOD, "R"],
                                   ["L", "F", TokenType.T_ID, TokenType.T_OPEN_BRACE],["L", TokenType.T_ID, "H",TokenType.T_SEMICOLON],
                                   ["D", TokenType.T_BOOL, TokenType.T_ID, TokenType.T_ASSIGN, "E"],
                                   ["D", TokenType.T_INT, TokenType.T_ID, TokenType.T_ASSIGN, "E"],
                                   ["D", TokenType.T_STRING, TokenType.T_ID, TokenType.T_ASSIGN, "E"],
                                   ["D", TokenType.T_DOUBLE, TokenType.T_ID, TokenType.T_ASSIGN, "E"],
                                   ["D", TokenType.T_ARRAY, "^"],
                                   ["T", TokenType.T_STRING], ["T", TokenType.T_INT],
                                   ["T", TokenType.T_DOUBLE], ["T", TokenType.T_BOOL],
                                   ["R", "K", TokenType.T_ID, TokenType.T_OPEN_PAREN,
                                    "P", TokenType.T_CLOSE_PAREN, TokenType.T_OPEN_BRACE], ["K", "T"],
                                   ["K", TokenType.T_VOID], ["P", "T", TokenType.T_ID, "~"], ["P", "e"],
                                   ["~", TokenType.T_COMMA, "T", TokenType.T_ID, "~"], ["~", "e"],
                                   ["@", TokenType.T_IF, TokenType.T_OPEN_PAREN, "G", TokenType.T_CLOSE_PAREN,
                                    TokenType.T_OPEN_BRACE],
                                   ["@", TokenType.T_WHILE, TokenType.T_OPEN_PAREN, "G", TokenType.T_CLOSE_PAREN,
                                    TokenType.T_OPEN_BRACE], ["N", TokenType.T_ELSE, TokenType.T_OPEN_BRACE],
                                   ["N", TokenType.T_ELIF, TokenType.T_OPEN_PAREN, "G", TokenType.T_CLOSE_PAREN,
                                    TokenType.T_OPEN_BRACE], ["N", "e"], ["W", TokenType.T_CONTINUE],
                                   ["W", TokenType.T_BREAK], ["W", TokenType.T_RETURN,"E"], ["F", TokenType.T_RIDER],
                                   ["F", TokenType.T_BIKE],
                                   ["A", TokenType.T_OPEN_PAREN, "Z", TokenType.T_CLOSE_PAREN], ["A", "e"],
                                   ["Z", "e"],["Z", "E","U"],["I",TokenType.T_ASSIGN],
                                   ["I", TokenType.T_ADD_AS], ["I", TokenType.T_SUB_AS], ["I", TokenType.T_DIV_AS],
                                   ["I", TokenType.T_MUL_AS], ["I", TokenType.T_MOD_AS], ["I", TokenType.T_EXP_AS],
                                   ["I",TokenType.T_AND_AS],["I",TokenType.T_OR_AS],["I",TokenType.T_XOR_AS],
                                   ["Q",TokenType.T_S_VALUE],["Q",TokenType.T_I_VALUE],["Q",TokenType.T_D_VALUE],["Q",TokenType.T_TRUE],
                                   ["Q",TokenType.T_FALSE],["Q",TokenType.T_ID,"A"], ["C", TokenType.T_GREQ_REL],
                                   ["C", TokenType.T_GREAT_REL], ["C", TokenType.T_LESS_REL],
                                   ["C", TokenType.T_LEQ_REL],["C",TokenType.T_EQ_REL], ["C",TokenType.T_NEQ_REL], ["M","Q"], ["M",TokenType.T_OPEN_PAREN, "E", TokenType.T_CLOSE_PAREN],
                                   ["Y","e"], ["Y",TokenType.T_MUL_OP, "M", "Y"],["Y",TokenType.T_DIV_OP, "M", "Y"],["Y",TokenType.T_MOD_OP, "M", "Y"],["Y",TokenType.T_EXP_OP, "M", "Y"],
                                   ["J", "e"], ["J", "O", "S"], ["U", "e"],
                                   ["U", TokenType.T_COMMA, "E", "U"],["X",TokenType.T_ADD_OP, "B","X"], ["X",TokenType.T_SUB_OP,"B","X"],
                                   ["X","e"], ["E", "B","X"], ["B", "M","Y"], ["G", "E","J"], ["S", "e"],
                                   ["S", TokenType.T_OR_OP, "G"], ["S", TokenType.T_AND_OP, "G"], ["S", TokenType.T_XOR_OP, "G"],
                                   ["^", "T", TokenType.T_ID, TokenType.T_ASSIGN,
                                    TokenType.T_OPEN_BRACKET, "E", "U", TokenType.T_CLOSE_BRACKET], ["H","I","E"],["H",TokenType.T_OPEN_PAREN, "Z"
                                    ,TokenType.T_CLOSE_PAREN],["O","C","E"],["O","e"]]
        self.first_producciones_calculado = False  # Esta variable booleana me sirve calcular los first restantes que luego me hacen falta para los Follows
        self.hacer_first("L")
        self.calcular_first_restantes()
        self.hacer_follow()
        self.completar_follows()
        self.construir_tabla_LL()
        self.error = None
        #self.variables = dict()  # Scope de variables

        # los terminales de la gramatica son estos que guardamos en el diccionario Terminales junto a las variables
        # y funciones que se guardan a medida que se crean en el diccionario Variables ,con su tipo , si se guarda una funcion
        # se guardaria primero los tipos de los parametros de dicha funcion y luego el tipo de retorno.

    # def parsing(tokens:[Token]))

    def hacer_first(self, cadena: str):
        if self.first.keys().isdisjoint(cadena):
            self.first[cadena] = []
        i = 0
        for prod in self.producciones[cadena]:
         
            self.first[self.key(prod)] = []
            if self.no_terminales.count(prod[i]) == 1:
                self.hacer_first(prod[i])
                self.first[cadena] += self.first[prod[i]]
                if len(prod) > 1:
                 self.first[self.key(prod)] += self.first[prod[i]]
                while self.se_va_en_epsilon(prod[i]):
                    i += 1
                    if i == len(prod):
                        break
                    if self.no_terminales.count(prod[i]) == 1:
                        self.hacer_first(prod[i])
                        self.first[cadena] += self.first[prod[i]]
                        self.first[self.key(prod)] += self.first[prod[i]]
                    else:
                        self.first[cadena].append(prod[i])
                        break
                i = 0
            else:
                if self.first[cadena].count(prod[i]) == 0:
                    self.first[cadena].append(prod[i])
                if not self.first_producciones_calculado:
                    self.first[self.key(prod)].append(prod[i])

    @staticmethod
    def key(produccion: list) -> str:
        prod_str = ""
        for i in range(len(produccion)):
            prod_str += "'" + produccion[i].name + "'" if isinstance(produccion[i], TokenType) else  produccion[i]
        return prod_str

    def se_va_en_epsilon(self, no_terminal) -> bool:
        if self.no_terminales.count(no_terminal) != 1:
            return no_terminal == "e"
        else:
            for prod in self.producciones[no_terminal]:
                i = 0
                while i < len(prod):
                    if not self.se_va_en_epsilon(prod[i]):
                        break
                    i += 1
                if i == len(prod):
                    return True
            return False

    def calcular_first_restantes(self):
        for nt in self.no_terminales:
            if self.first.keys().isdisjoint(nt):
                self.hacer_first(nt)

    def hacer_follow(self):
        terminales_para_follow = list()  # Aqui voy teniendo los posibles terminales que pueden pertenecer al follow de los no terminales que voy revisando
        for prod in self.lista_producciones:
            terminales_para_follow.clear()
            existe_ultimo_terminal = True  # Esta variable es para identificar los casos en que lo ultimo que me queda en mi produccion pueda ser un No terminal y por lo tanto el Follow de la cabeza de la produccion sera subconjunyto del Follow del no terminal
            for i in range(len(prod) - 1, 0, -1):
                if self.no_terminales.count(prod[i]) == 1:
                    if len(terminales_para_follow) > 0:
                        self.follow[prod[i]] = list(set(self.follow[prod[i]] + terminales_para_follow))
                    if existe_ultimo_terminal:
                        if prod[0]!=prod[i] and self.pendiente_follow.count("{},{}".format(prod[0], prod[i]))==0:
                         self.pendiente_follow.append("{},{}".format(prod[0], prod[i])) 
                    if self.se_va_en_epsilon(prod[i]):
                        terminales_para_follow += self.first[prod[i]]
                        if terminales_para_follow.count(prod[i]) == 1:
                            terminales_para_follow.remove("e")
                    else:
                        terminales_para_follow.clear()
                        terminales_para_follow += self.first[prod[i]]
                        if terminales_para_follow.count(prod[i]) == 1:
                            terminales_para_follow.remove("e")
                        existe_ultimo_terminal = False
                else:
                    existe_ultimo_terminal = False
                    terminales_para_follow.clear()
                    if prod[i] != "e" and terminales_para_follow.count(prod[i]) == 0:
                        terminales_para_follow.append(prod[i])

    def AjustaFollows(self,cabeza,ultimoterminal):
       if cabeza!=ultimoterminal:
        for x in self.completafollow[ultimoterminal]:
            self.follow[x] = list(self.follow[x] + self.follow[cabeza])
            self.AjustaFollows(cabeza,x)

    def completar_follows(self):
        for follow in self.pendiente_follow:
            self.follow[follow[2]] = list(self.follow[follow[2]] + self.follow[follow[0]])
            self.completafollow[follow[0]]+= follow[2]
            self.AjustaFollows(follow[0],follow[2])

         

    def construir_tabla_LL(self):
        fila = 0
        for nt in self.no_terminales:
            columna = 0
            for t in self.terminales:
                if t != "e":
                    for i in range(len(self.producciones[nt])):
                        esta = self.first.get(self.key(self.producciones[nt][i]), "NoEsta")
                        if esta != "NoEsta" and self.first[self.key(self.producciones[nt][i])].count(t) > 0:
                            self.matriz[fila][columna] = self.producciones[nt][i]
                            break
                if self.follow[nt].count(t) > 0 and self.se_va_en_epsilon(nt) and self.matriz[fila][columna] is None:
                    self.matriz[fila][columna] = "e"
                columna += 1
            fila += 1

    def parsear(self, line, cadena):        
        self.error = None      
        for termino in cadena:
            
            if self.i < len(line):
                if self.i == 0:
                    if len(self.estados) != 0:
                        estado = self.estados[- 1]
                        if estado == Region.R_TYPE:
                            if line[self.i].token_type != TokenType.T_METHOD and line[self.i].token_type !=TokenType.T_CLOSE_BRACE:
                                self.error = UnexpectedCharacterError("Wrong token in this scope", "", line[self.i].line, line[self.i].column)#
                                return False
                        elif estado == Region.R_IF or estado == Region.R_ELIF or estado == Region.R_ELSE:
                            if line[self.i].token_type == TokenType.T_METHOD or line[self.i].token_type ==TokenType.T_BIKE or line[self.i].token_type ==TokenType.T_RIDER:
                                self.error = UnexpectedCharacterError("Wrong token in this scope", "", line[self.i].line, line[self.i].column)#
                                return False
                        elif estado == Region.R_WHILE:
                            if line[self.i].token_type == TokenType.T_METHOD or line[self.i].token_type == TokenType.T_BIKE or line[self.i].token_type == TokenType.T_RIDER:
                                self.error = UnexpectedCharacterError("Wrong token in this scope", "", line[self.i].line, line[self.i].column)#
                                return False
                        elif estado == Region.R_METHOD:
                            if line[self.i].token_type == TokenType.T_METHOD or line[self.i].token_type == TokenType.T_BIKE or line[self.i].token_type == TokenType.T_RIDER or line[self.i].token_type == TokenType.T_CONTINUE or line[self.i].token_type == TokenType.T_BREAK:
                                self.error = UnexpectedCharacterError("Wrong token in this scope", "", line[self.i].line, line[self.i].column)#
                                return False
                
                    else:
                        if line[self.i].token_type == TokenType.T_CONTINUE or line[self.i].token_type == TokenType.T_BREAK or line[self.i].token_type == TokenType.T_RETURN:
                                self.error = UnexpectedCharacterError("Wrong token in this scope", "", line[self.i].line, line[self.i].column)#
                                return False

                if termino == line[self.i].token_type:
                    if line[self.i].token_type == TokenType.T_RIDER or line[self.i].token_type == TokenType.T_BIKE:
                        self.estados.append(Region.R_TYPE)
                    elif line[self.i].token_type == TokenType.T_METHOD:
                        self.estados.append(Region.R_METHOD)
                    elif line[self.i].token_type == TokenType.T_WHILE:
                        self.estados.append(Region.R_WHILE)
                    elif line[self.i].token_type == TokenType.T_IF:
                        self.estados.append(Region.R_IF)
                    elif line[self.i].token_type == TokenType.T_ELIF:
                        if self.estados[- 1] == Region.R_IF or  self.estados[- 1]==Region.R_ELIF:
                            self.estados.pop()
                            self.estados.append(Region.R_ELIF)
                        else:
                            self.error = UnexpectedCharacterError("The Elif region can only come after an IF region or an Elif region", "", line[self.i].line, line[self.i].column)#
                            return False
                    elif line[self.i].token_type == TokenType.T_ELSE:
                        if self.estados[- 1] == Region.R_IF or self.estados[- 1] ==Region.R_ELIF:
                            self.estados.pop()
                            self.estados.append(Region.R_ELSE)
                        else:
                            self.error =UnexpectedCharacterError("The Else region can only come after an IF region or an Elif region", "", line[self.i].line, line[self.i].column)#
                            return False
                    elif line[self.i].token_type == TokenType.T_CLOSE_BRACE:
                        if self.i + 1 == len(line) or (self.estados[- 1] != Region.R_IF and self.estados[- 1] != Region.R_ELIF):
                           try:
                            self.estados.pop()
                           except:
                              self.error= UnbalancedBracketsError("unexpected end of region","",line[self.i].line, line[self.i].column)
                              return False
                    self.EligeTipoDdeclaracion(termino,line[self.i],line)
                    self.i += 1
                    continue
                elif isinstance(termino, TokenType):
                    self.error = UnexpectedCharacterError("Wrong token in this string", "", line[self.i].line, line[self.i].column)# Aqui nunca va a entrar , solo si esta mal la matriz
                    return False
                indice_nt = self.no_terminales.index(termino)
                indice_t = self.terminales.index(line[self.i].token_type)
                
                
                self.EligeTipoDdeclaracion(termino,line[self.i],line)
                if self.matriz[indice_nt][indice_t] != None  :
                    if self.matriz[indice_nt][indice_t]!="e":
                      if self.parsear(line, self.matriz[indice_nt][indice_t])==False:
                             return False
                    if self.estadoDAST==EstadoDAST.EnExpresionAssign and termino!="A" and termino!="U" and termino!="Z" and termino!="H":
                         self.nodoactual.nododreconocimiento.refreshAST()
                         if self.nodoactual.noderaiz.ast!= None:
                             self.RectificaEstado()
                             if not isinstance(self.nodoactual.padre,ReturnNode): 
                              self.nodoactual=self.nodoactual.padre
                             else:
                                 self.nodoactual=self.nodoactual.padre.padre
                         elif self.nodoactual.nododreconocimiento.padre!=None:
                            self.nodoactual.nododreconocimiento= self.nodoactual.nododreconocimiento.padre
                elif self.matriz[indice_nt][indice_t] != "e":
                    self.error=UnexpectedCharacterError("Wrong string in this language", "", line[self.i].line, line[self.i].column)##Aqui debemos agregar el error , con ello la linea y la columna que fue para posteriormente comunicarselo al usuario
                    return False
            else:
                break

        

    
    def parse(self, lines: [[Token]]) -> Error:
        for line in lines:
            self.parsear(line, "L")
            self.i=0
            if self.error!=None:
              return self.error
        
        return True
    
    def CreaNododProgram(self,line,termino,token):
        if termino=="D":
            nuevonodo = D_Assign()
            nuevonodo.token=token
            self.nodoactual.statements.append(nuevonodo)
            nuevonodo.padre=self.nodoactual
            self.nodoactual=nuevonodo
            self.estadoDAST=EstadoDAST.EnAsignacion
        elif termino==TokenType.T_METHOD:
            nuevonodo= Def_Fun()
            nuevonodo.token=token
            self.nodoactual.statements.append(nuevonodo)
            nuevonodo.padre=self.nodoactual
            self.nodoactual=nuevonodo
            self.estadoDAST=EstadoDAST.EnFuncion
        elif termino== TokenType.T_RIDER or  termino==TokenType.T_BIKE:
            if termino == TokenType.T_RIDER:
                nuevonodo=RiderNode()
                nuevonodo.token=token               
            else:
                
                nuevonodo=MotorcicleNode()
                nuevonodo.token=token
            nuevonodo.padre=self.nodoactual
            self.nodoactual.statements.append(nuevonodo)
            self.nodoactual=nuevonodo
            self.estadoDAST=EstadoDAST.EnTipoEspecial
        elif termino== TokenType.T_IF :
            nuevonodo= IfCond()
            self.nodoactual.statements.append(nuevonodo)
            nuevonodo.padre=self.nodoactual
            self.nodoactual=nuevonodo
            self.estadoDAST=EstadoDAST.EnCondicionIf
        elif termino == TokenType.T_WHILE :
            nuevonodo = WhileCond()
            self.nodoactual.statements.append(nuevonodo)
            nuevonodo.padre=self.nodoactual
            self.nodoactual=nuevonodo
            self.estadoDAST=EstadoDAST.EnWhile
        elif termino == TokenType.T_RETURN or termino == TokenType.T_BREAK or termino == TokenType.T_CONTINUE :
            nuevonodo = ReturnNode()
            nuevonodo.token=token
            nuevonodo.padre=self.nodoactual            
            self.nodoactual.statements.append(nuevonodo)
            
            if termino == TokenType.T_RETURN:
                 nuevonodo.type="return"                 
                 self.nodoactual=nuevonodo
                 nodoparaExpression=Expression()
                 nodoparaExpression.padre=self.nodoactual
                 self.nodoactual.expr=nodoparaExpression
                 self.nodoactual=nodoparaExpression
                 self.estadoDAST=EstadoDAST.EnExpresionAssign

            elif termino == TokenType.T_BREAK:
                nuevonodo.type="break"
            else:
                nuevonodo.type="continue"                        
            
        elif termino == TokenType.T_ID :
          if self.i+1<len(line):
           if line[self.i+1].token_type== TokenType.T_OPEN_PAREN:
               nuevonodo= FunCall()
               nuevonodo.token=token
               nuevonodo.id= token.value
               nuevonodo.padre=self.nodoactual
               self.nodoactual.statements.append(nuevonodo)
               self.nodoactual=nuevonodo
               self.estadoDAST=EstadoDAST.LlamadoAfuncion
           else: 
                 nuevonodo = Redefinition()
                 nuevonodo.token=token
                 self.nodoactual.statements.append(nuevonodo)
                 nuevonodo.padre=self.nodoactual
                 self.nodoactual=nuevonodo
                 self.nodoactual.id=token.value
                 self.estadoDAST=EstadoDAST.EnRedefinition
        elif termino == TokenType.T_CLOSE_BRACE :
            self.nodoactual= self.nodoactual.padre
            if isinstance(self.nodoactual,IfCond):
              if self.i+1 == len(line):
                 while isinstance(self.nodoactual,IfCond): 
                  self.nodoactual=self.nodoactual.padre
                 self.estadoDAST=EstadoDAST.EnProgram
              else:
               self.estadoDAST=EstadoDAST.EnCondicionIf
            if isinstance(self.nodoactual,WhileCond):
              self.nodoactual=self.nodoactual.padre
              self.estadoDAST=EstadoDAST.EnProgram
              
            if isinstance(self.nodoactual,Def_Fun):
                 if isinstance(self.nodoactual.padre,Program):
                     self.estadoDAST=EstadoDAST.EnProgram
                 else:
                     self.estadoDAST=EstadoDAST.EnTipoEspecial
                 self.nodoactual=self.nodoactual.padre
    def EligeTipoDdeclaracion(self,termino,token:Token,line):
        if self.estadoDAST==EstadoDAST.EnAsignacion:
            self.CreaNododAsignacion(termino,token)
        elif self.estadoDAST==EstadoDAST.EnExpresionAssign:
            self.CreaNododExpresion(termino,token,line)
        elif self.estadoDAST==EstadoDAST.EnProgram:
            self.CreaNododProgram(line,termino,token)
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
        elif self.estadoDAST==EstadoDAST.EnTipoEspecial:
            self.CreanodoTipoEspecial(termino,token)
  
    
    def CreanodoTipoEspecial(self,termino,token):
         if termino==TokenType.T_ID:
             self.nodoactual.id=token.value
             return
         elif termino==TokenType.T_OPEN_BRACE or termino==TokenType.T_METHOD:
             self.estadoDAST=EstadoDAST.EnFuncion
             nuevonodo= Def_Fun()
             nuevonodo.token=token
             self.nodoactual.funciones.append(nuevonodo)
             nuevonodo.padre=self.nodoactual
             self.nodoactual=nuevonodo
         elif termino==TokenType.T_CLOSE_BRACE:
             self.nodoactual=self.nodoactual.padre
             self.estadoDAST=EstadoDAST.EnProgram

    def CreaNododAsignacion(self,termino,token:Token):
        if termino==TokenType.T_INT :
            self.nodoactual.typevar=VariableType.INT
        elif termino==TokenType.T_BOOL :
            self.nodoactual.typevar=VariableType.BOOL
        elif termino==TokenType.T_DOUBLE :
            self.nodoactual.typevar=VariableType.DOUBLE
        elif termino==TokenType.T_ID :
             self.nodoactual.id = token.value
        elif termino==TokenType.T_ASSIGN :
           nuevonodo=Expression()
           if not self.nodoactual.isarray:
            self.estadoDAST=EstadoDAST.EnExpresionAssign
            self.nodoactual.expr=nuevonodo
            nuevonodo.padre=self.nodoactual
            self.nodoactual=self.nodoactual.expr
           else :
             self.nodoactual.arrayvalue.append(nuevonodo)
             self.estadoDAST=EstadoDAST.EnExpresionAssign
             nuevonodo.padre=self.nodoactual
             self.nodoactual= nuevonodo

        elif termino==TokenType.T_STRING:
            self.nodoactual.typevar=VariableType.STRING
        elif termino==TokenType.T_ARRAY:
            self.nodoactual.isarray=True
        elif termino==TokenType.T_COMMA:
            nuevonodo=Expression()
            self.nodoactual.arrayvalue.append(nuevonodo)
            self.estadoDAST=EstadoDAST.EnExpresionAssign
            nuevonodo.padre=self.nodoactual
            self.nodoactual= nuevonodo
        elif termino==TokenType.T_SEMICOLON :
            self.estadoDAST=EstadoDAST.EnProgram
            self.nodoactual= self.nodoactual.padre


    def CreanodoCall(self,termino,token:Token):
        if termino=="E":
            
            if isinstance(self.nodoactual,Expression):
             nuevonodo=NodeE()
             nuevonodo.padre=self.nodoactual.nododreconocimiento
             self.nodoactual.nododreconocimiento.args.append(nuevonodo)
             self.nodoactual.nododreconocimiento=nuevonodo
            else:
             nuevonodo= Expression()
             nuevonodo.padre=self.nodoactual
             self.nodoactual.args.append(nuevonodo)
             self.nodoactual=nuevonodo
            self.estadoDAST=EstadoDAST.EnExpresionAssign

            
    def CreaArgsdfun(self,termino,token:Token):
        if termino==TokenType.T_INT :
            self.nodoactual.args.append([VariableType.INT])
        if termino==TokenType.T_ID :
            self.nodoactual.args[len(self.nodoactual.args)-1].append(token.value)
        elif termino==TokenType.T_BOOL :
            self.nodoactual.args.append([VariableType.BOOL])
        elif termino==TokenType.T_DOUBLE :
            self.nodoactual.args.append([VariableType.DOUBLE])
        elif termino==TokenType.T_STRING:
            self.nodoactual.args.append([VariableType.STRING])
        elif termino==TokenType.T_CLOSE_PAREN:
            self.estadoDAST=EstadoDAST.EnFuncion

    def CreanodoDredefinition(self,termino,token:Token):
        if termino==TokenType.T_ASSIGN :
            nuevonodo=Assign(self.nodoactual.id)
            nuevonodo.token=token
        elif termino==TokenType.T_ADD_AS :
            nuevonodo=AddAs(self.nodoactual.id)
            nuevonodo.token=token
        elif termino==TokenType.T_SUB_AS :
            nuevonodo=SubAs(self.nodoactual.id)
            nuevonodo.token=token
        elif termino==TokenType.T_MUL_AS :
            nuevonodo=MulAs(self.nodoactual.id)
            nuevonodo.token=token
        elif termino==TokenType.T_DIV_AS :
            nuevonodo=DivAs(self.nodoactual.id)
            nuevonodo.token=token
        elif termino==TokenType.T_MOD_AS :
            nuevonodo=ModAs(self.nodoactual.id)
            nuevonodo.token=token
        elif termino==TokenType.T_EXP_AS :
            nuevonodo=ExpAs(self.nodoactual.id)
            nuevonodo.token=token
        elif termino==TokenType.T_AND_AS :
            nuevonodo=AndAs(self.nodoactual.id)
            nuevonodo.token=token
        elif termino==TokenType.T_OR_AS :
            nuevonodo=OrAs(self.nodoactual.id)
            nuevonodo.token=token
        elif termino==TokenType.T_XOR_AS :
            nuevonodo=XorAs(self.nodoactual.id)
            nuevonodo.token=token
        elif termino==TokenType.T_SEMICOLON :
            self.estadoDAST=EstadoDAST.EnProgram
            self.nodoactual= self.nodoactual.padre
            return
        if termino!="I" and termino!="H":
         self.nodoactual.op=nuevonodo
         self.estadoDAST=EstadoDAST.EnExpresionAssign
         nodoexpression=Expression()
         self.nodoactual.expr=nodoexpression
         self.nodoactual.op.expression=nodoexpression
         nodoexpression.padre=self.nodoactual
         self.nodoactual=self.nodoactual.expr

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
            nodonuevo= Program()
            nodonuevo.token=token
            nodonuevo.padre=self.nodoactual
            self.nodoactual.body=nodonuevo
            self.nodoactual=nodonuevo
            self.nodoactual.isfuncion=True
            self.estadoDAST=EstadoDAST.EnProgram
            
    def CreaNododIf(self,termino,token:Token):
           if termino == TokenType.T_OPEN_BRACE:
               nuevonodo=Program()
               nuevonodo.token=token
               nuevonodo.padre=self.nodoactual
               self.nodoactual.body=nuevonodo
               self.nodoactual=nuevonodo
               self.estadoDAST=EstadoDAST.EnProgram
           elif termino==TokenType.T_OPEN_PAREN:
               self.estadoDAST=EstadoDAST.Condicion
               nuevonodo= Condition()
               nuevonodo.token=token
               nuevonodo.padre=self.nodoactual
               self.nodoactual=nuevonodo
           elif termino==TokenType.T_ELIF: 
               nuevonodo = IfCond() 
               nuevonodo.padre=self.nodoactual
               self.nodoactual.nodoelse=nuevonodo
               self.nodoactual=nuevonodo  
           elif termino==TokenType.T_ELSE:
               nuevonodo = Program() 
               nuevonodo.token=token
               nuevonodo.padre=self.nodoactual
               self.nodoactual.nodoelse=nuevonodo
               self.nodoactual=nuevonodo
               self.estadoDAST=EstadoDAST.EnProgram

    def CreaNodoCondicion(self,termino,token:Token):
         if termino==TokenType.T_EQ_REL or termino==TokenType.T_NEQ_REL or termino==TokenType.T_LESS_REL or termino==TokenType.T_LEQ_REL or termino==TokenType.T_GREAT_REL or  termino==TokenType.T_GREQ_REL:
             if termino==TokenType.T_EQ_REL:
                 self.nodoactual.comparador=EqRel(self.nodoactual.expression1,self.nodoactual.expression2)
             if termino==TokenType.T_NEQ_REL:
                 self.nodoactual.comparador=NeqRel(self.nodoactual.expression1,self.nodoactual.expression2)
             if termino==TokenType.T_LESS_REL:
                 self.nodoactual.comparador=LessRel(self.nodoactual.expression1,self.nodoactual.expression2)
             if termino==TokenType.T_LEQ_REL:
                 self.nodoactual.comparador=LeqRel(self.nodoactual.expression1,self.nodoactual.expression2)
             if termino==TokenType.T_GREAT_REL:
                 self.nodoactual.comparador=GreatRel(self.nodoactual.expression1,self.nodoactual.expression2)
             if termino==TokenType.T_GREQ_REL:   
               self.nodoactual.comparador=GreqRel(self.nodoactual.expression1,self.nodoactual.expression2)                 
             nuevonodo=Expression()
             self.nodoactual.expression2 = nuevonodo
             self.nodoactual.comparador.right_node=nuevonodo
             nuevonodo.padre=self.nodoactual
             self.nodoactual=nuevonodo
             self.nodoactual.noderaiz=self.nodoactual.nododreconocimiento
             self.estadoDAST=EstadoDAST.EnExpresionAssign
         elif termino=="E":                       
             nuevonodo=Expression()
             self.nodoactual.expression1= nuevonodo
             nuevonodo.padre=self.nodoactual
             self.nodoactual=nuevonodo
             self.nodoactual.noderaiz=self.nodoactual.nododreconocimiento
             self.estadoDAST=EstadoDAST.EnExpresionAssign
         elif termino==TokenType.T_CLOSE_PAREN or termino==TokenType.T_OR_OP or termino==TokenType.T_AND_OP or termino==TokenType.T_XOR_OP:
              self.nodoactual.padre.conditions.append(self.nodoactual)
              if termino==TokenType.T_CLOSE_PAREN:
                     self.estadoDAST=EstadoDAST.EnCondicionIf
                     self.nodoactual=self.nodoactual.padre
              else :

                  if termino==TokenType.T_OR_OP :
                   self.nodoactual.padre.operadoresbinarios.append(OrOp(None,None))
                  elif termino==TokenType.T_AND_OP:
                   self.nodoactual.padre.operadoresbinarios.append(AndOp(None,None))
                  elif termino==TokenType.T_XOR_OP:
                   self.nodoactual.padre.operadoresbinarios.append(XorOp(None,None))
                  nodopadre=self.nodoactual.padre
                  self.estadoDAST=EstadoDAST.EnExpresionAssign
                  self.nodoactual= Condition()
                  self.nodoactual.token=token
                  self.nodoactual.padre=nodopadre

                  nuevonodo=Expression()
                  self.nodoactual.expression1 = nuevonodo
                  nuevonodo.padre=self.nodoactual
                  self.nodoactual=nuevonodo
                  self.nodoactual.noderaiz=self.nodoactual.nododreconocimiento
            


    def CreaNododExpresion(self,termino,token:Token,line):
        
      if termino!="G"  :
        
       # if termino==TokenType.T_CLOSE_BRACKET and line[self.i-1]==TokenType.T_ASSIGN:
            
        if termino==TokenType.T_ADD_OP:
            nuevonodo=AddOp(Node(),Node())
            nuevonodo.token=token
        elif termino==TokenType.T_SUB_OP:
            nuevonodo=SubOp(Node(),Node())
            nuevonodo.token=token
        elif termino==TokenType.T_MUL_OP:
            nuevonodo=MulOp(Node(),Node())
            nuevonodo.token=token
        elif termino==TokenType.T_DIV_OP:
            nuevonodo=DivOp(Node(),Node())
            nuevonodo.token=token
        elif termino==TokenType.T_MOD_OP:
            nuevonodo=ModOp(Node(),Node())
            nuevonodo.token=token
        elif termino==TokenType.T_EXP_OP:
            nuevonodo=Exp(Node(),Node())
            nuevonodo.token=token
        elif termino==TokenType.T_COMMA:
             self.estadoDAST=EstadoDAST.LlamadoAfuncion
             if isinstance(self.nodoactual.padre,FunCall):
                 self.nodoactual=self.nodoactual.padre
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
            if termino==TokenType.T_CLOSE_PAREN and isinstance(self.nodoactual,FunCall) :
                self.nodoactual = self.nodoactual.padre
                return
            elif termino==TokenType.T_CLOSE_PAREN and isinstance(self.nodoactual.nododreconocimiento,FunCall):
                  self.nodoactual.nododreconocimiento = self.nodoactual.nododreconocimiento.padre 
                  return
            else :
             nuevonodo=Nodepsilon()
        elif termino== TokenType.T_D_VALUE or termino==TokenType.T_I_VALUE or termino==TokenType.T_S_VALUE or termino==TokenType.T_FALSE or termino==TokenType.T_TRUE  :
            nuevonodo=Val(token)
        elif termino==TokenType.T_ID:
            if len(line)-1==self.i:
                nuevonodo=Variable(token)
            elif line[self.i+1].token_type==TokenType.T_OPEN_PAREN:
                 nuevonodo=FunCall()
                 nuevonodo.token=token
                 nuevonodo.id= token.value
                 self.estadoDAST=EstadoDAST.LlamadoAfuncion
            else:  
                 nuevonodo=Variable(token)
        if termino!=TokenType.T_OPEN_BRACKET and termino!="U":
          if isinstance(self.nodoactual.nododreconocimiento,NodeE) and isinstance(nuevonodo,NodeE) :
            self.nodoactual.nododreconocimiento=nuevonodo
            self.nodoactual.noderaiz=nuevonodo
          elif termino!="A" and termino!="Z" and termino!="U":
            nuevonodo.padre=self.nodoactual.nododreconocimiento
            self.nodoactual.nododreconocimiento.hijos.append(nuevonodo)
            if termino == "E" or termino=="B" or termino=="M"or termino=="X" or termino=="Y" or termino=="Q" or isinstance(nuevonodo,FunCall) :
             self.nodoactual.nododreconocimiento=nuevonodo

    def RectificaEstado(self):
       if isinstance(self.nodoactual.padre,Condition):
         self.estadoDAST=EstadoDAST.Condicion # Metodo para subir en el ast
       elif isinstance(self.nodoactual.padre,D_Assign) :
            self.estadoDAST=EstadoDAST.EnAsignacion   
       elif isinstance(self.nodoactual.padre,Redefinition) :
            self.estadoDAST=EstadoDAST.EnRedefinition
         # Metodo para subir en el ast   
       elif isinstance(self.nodoactual.padre,Program):
         self.estadoDAST=EstadoDAST.EnProgram # Metodo para subir en el ast
       elif isinstance(self.nodoactual.padre,ReturnNode):
         self.estadoDAST=EstadoDAST.EnProgram 
       elif isinstance(self.nodoactual.padre,FunCall):
         self.estadoDAST=EstadoDAST.LlamadoAfuncion
       elif isinstance(self.nodoactual.padre,RiderNode) or isinstance(self.nodoactual.padre,MotorcicleNode) :
         self.estadoDAST=EstadoDAST.EnTipoEspecial

    
         
    def validaAST(self):
        for statement in self.nodopararecorrerast.statements:
            validationstatement=statement.validate(self.context)
            if not isinstance(validationstatement,bool):
                return validationstatement
        return True

    def checktypes(self):
        for statement in self.nodopararecorrerast.statements:
            checkstatement=statement.checktype(self.context)
            if not isinstance(checkstatement,bool):
                return checkstatement
        return True

    def execute(self):
        self.nodopararecorrerast.eval(self.context)


    def LoadRidersAndBikes(self):
        for statement in self.nodopararecorrerast.statements:
            if isinstance(statement,RiderNode):
                self.Riders.append(statement)
            elif isinstance(statement,MotorcicleNode):
                self.Motorcicles.append(statement)