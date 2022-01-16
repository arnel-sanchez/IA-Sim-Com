from compilation.errors import Error
from compilation.tokens import TokenType, Token
from compilation.enums import Region,EstadoDAST,VariableType,MethodType
from compilation.ast.nodes import *
from compilation.ast.relations import *
from compilation.ast.assignments import *
from compilation.ast.operations import *


class Parser:
    def __init__(self):
        self.estados = []  # Aqui guardamos los estados en forma de string , de forma que si el ultimo estado de la lista es el estado en el que estoy y si no hay estados en la lista ent estamos fuera de cualquier ambito del programa
        self.context=Context()
        self.i=0
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
                             "F": [[TokenType.T_RIDER], [TokenType.T_MOTORCYCLE]],
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
                             "J": [["e"], ["C", "E", "S"]],
                             "U": [["e"], [TokenType.T_COMMA, "E", "U"]],
                             "X": [[TokenType.T_ADD_OP, "B","X"], [TokenType.T_SUB_OP,"B","X"],["e"]],
                             "E": [["B","X"]],
                             "B": [["M","Y"]],
                             "G": [["E","J"]],
                             "S": [["e"],[TokenType.T_OR_OP,"G"],[TokenType.T_AND_OP,"G"]],
                             "^": [["T", TokenType.T_ID, TokenType.T_ASSIGN, TokenType.T_OPEN_BRACKET,
                                    "E", "U", TokenType.T_CLOSE_BRACKET]],
                             "H": [[ "I","E"],[TokenType.T_OPEN_PAREN, "Z"
                                    ,TokenType.T_CLOSE_PAREN]]} 
                                  
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
                           TokenType.T_MOTORCYCLE]
        self.no_terminales = ["L", "D", "I", "E", "M", "Y", "J", "U", "N", "@", "R", "K", "T", "P", "W", "S", "F",
                              "A", "Z", "Q", "C", "B", "G", "X", "~", "^","H"]
        self.first = dict()  # Guardamos los terminales que pertenecen al First de cada produccion posible de nuestra gramatica
        self.follow = {"L": [], "D": [], "I": [], "E": [], "M": [], "Y": [], "J": [], "U": [], "N": [], "@": [],
                       "R": [], "K": [], "T": [], "P": [], "W": [], "S": [], "F": [], "A": [], "Z": [],
                        "Q": [], "C": [], "B": [], "G": [], "X": [], "~": [],
                       "^": [],"H": []}
                                
        self.completafollow = {"L": [], "D": [], "I": [], "E": [], "M": [], "Y": [], "J": [], "U": [], "N": [], "@": [],
                       "R": [], "K": [], "T": [], "P": [], "W": [], "S": [], "F": [], "A": [], "Z": [],
                        "Q": [], "C": [], "B": [], "G": [], "X": [], "~": [],
                       "^": [], "H":[]} 
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
                                   ["F", TokenType.T_MOTORCYCLE],
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
                                   ["J", "e"], ["J", "C", "E", "S"], ["U", "e"],
                                   ["U", TokenType.T_COMMA, "E", "U"],["X",TokenType.T_ADD_OP, "B","X"], ["X",TokenType.T_SUB_OP,"B","X"],
                                   ["X","e"], ["E", "B","X"], ["B", "M","Y"], ["G", "E","J"], ["S", "e"],
                                   ["S", TokenType.T_OR_OP, "G"], ["S", TokenType.T_AND_OP, "G"],
                                   ["^", "T", TokenType.T_ID, TokenType.T_ASSIGN,
                                    TokenType.T_OPEN_BRACKET, "E", "U", TokenType.T_CLOSE_BRACKET], ["H","I","E"],["H",TokenType.T_OPEN_PAREN, "Z"
                                    ,TokenType.T_CLOSE_PAREN]]
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
                            if line[self.i].token_type != (TokenType.T_METHOD and TokenType.T_CLOSE_BRACE):
                                self.error = Error("Error", "", "", 0, 0)#
                                break
                        elif estado == Region.R_IF or estado == Region.R_ELIF or estado == Region.R_ELSE:
                            if line[self.i].token_type == (TokenType.T_METHOD or TokenType.T_RETURN or TokenType.T_BREAK or
                                                      TokenType.T_CONTINUE or TokenType.T_MOTORCYCLE or
                                                      TokenType.T_RIDER):
                                self.error = Error("Error", "", "", 0, 0)#
                                break
                        elif estado == Region.R_WHILE:
                            if line[self.i].token_type == (TokenType.T_METHOD or TokenType.T_RETURN or
                                                      TokenType.T_MOTORCYCLE or TokenType.T_RIDER):
                                self.error = Error("Error", "", "", 0, 0)#
                                break
                if termino == line[self.i].token_type:
                    if line[self.i].token_type == (TokenType.T_RIDER or TokenType.T_MOTORCYCLE):
                        self.estados.append(Region.R_TYPE)
                    elif line[self.i].token_type == TokenType.T_METHOD:
                        self.estados.append(Region.R_METHOD)
                    elif line[self.i].token_type == TokenType.T_WHILE:
                        self.estados.append(Region.R_WHILE)
                    elif line[self.i].token_type == TokenType.T_IF:
                        self.estados.append(Region.R_IF)
                    elif line[self.i].token_type == TokenType.T_ELIF:
                        if self.estados[- 1] == (Region.R_IF or Region.R_ELIF):
                            self.estados.pop()
                            self.estados.append(Region.R_ELIF)
                        else:
                            self.error = Error("", "", "", 0, 0)#
                            break
                    elif line[self.i].token_type == TokenType.T_ELSE:
                        if self.estados[- 1] == Region.R_IF or self.estados[- 1] ==Region.R_ELIF:
                            self.estados.pop()
                            self.estados.append(Region.R_ELSE)
                        else:
                            self.error = Error("", "", "", 0, 0)#
                            break
                    elif line[self.i].token_type == TokenType.T_CLOSE_BRACE:
                        if self.i + 1 == len(line) or (self.estados[- 1] != Region.R_IF and self.estados[- 1] != Region.R_ELIF):
                            self.estados.pop()
                    
                    self.EligeTipoDdeclaracion(termino,line[self.i],line)
                    self.i += 1
                    continue
                elif isinstance(termino, TokenType):
                    self.error = Error("", "", "", 0, 0)#
                    break
                indice_nt = self.no_terminales.index(termino)
                indice_t = self.terminales.index(line[self.i].token_type)
                
                
                self.EligeTipoDdeclaracion(termino,line[self.i],line)
                if self.matriz[indice_nt][indice_t] != None  :
                    if self.matriz[indice_nt][indice_t]!="e":
                     self.parsear(line, self.matriz[indice_nt][indice_t])
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
                    
                    if self.error is not None:
                        break
                elif self.matriz[indice_nt][indice_t] != "e":
                    self.error = Error("", "", "", 0, 0)#Aqui debemos agregar el error , con ello la linea y la columna que fue para posteriormente comunicarselo al usuario
                    break
            else:
                break
    
    def parse(self, lines: [[Token]]) -> Error:
        for line in lines:
            self.parsear(line, "L")
            self.i=0
        return self.error

    def validaAST(self):
        for statement in self.nodopararecorrerast.statements:
            if not statement.validate(self.context):
                return False
        return True

    def checktypes(self):
        for statement in self.nodopararecorrerast.statements:
            if not statement.checktype(self.context):
                return False
        return True
