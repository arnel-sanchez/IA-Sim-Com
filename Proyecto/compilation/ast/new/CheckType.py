
from enum import Enum

class VariableType(Enum):
    STRING = 0
    INT = 1
    DOUBLE = 2
    BOOL = 3
    ARRAY = 4

class MethodType(Enum):
    VOID = 0
    STRING = 1
    INT = 2
    DOUBLE = 3
    BOOL = 4
    ARRAY = 5

class Context:    
    variables=dict()
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
                     return context.funciones[idvar][0]

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

class Error:
    def __init__(self, error_type: str, details: str, file: str, line: int, column: int):
        self.error_type = error_type
        self.details = details
        self.file = file
        self.line = line
        self.column = column

    def __repr__(self):
        return "{} ERROR: '{}', file {}, line {}, column {}".format(self.error_type, self.details, self.file,
                                                                    self.line, self.column)


class Node:


    def eval(self, variables: dict):
        return None

    def __repr__(self) -> str:
        return "NODE()"

class TokenType(Enum):
    T_SEMICOLON = 0  # ';'
    T_OPEN_PAREN = 1  # '('
    T_CLOSE_PAREN = 2  # ')'
    T_OPEN_BRACKET = 3  # '['
    T_CLOSE_BRACKET = 4  # ']'
    T_OPEN_BRACE = 5  # '{'
    T_CLOSE_BRACE = 6  # '}'
    T_COMMENT = 7  # '#'

    T_STRING = 8  # string
    T_INT = 9  # int
    T_DOUBLE = 10  # double
    T_BOOL = 11  # bool
    T_ARRAY = 61#

    T_NULL = 12  # null

    T_TRUE = 13  # true
    T_FALSE = 14  # false

    T_IF = 15  # if
    T_ELIF = 16  # elif
    T_ELSE = 17  # else

    T_WHILE = 18  # while
    T_CONTINUE = 19  # continue
    T_BREAK = 20  # break

    T_METHOD = 21  # method
    T_VOID = 22  # void
    T_RETURN = 23  # return

    T_INCLUDE = 24  # include

    T_ID = 25  # variables
    T_M_ID = 26  # methods

    T_S_VALUE = 27  # some string value
    T_I_VALUE = 28  # some int value
    T_D_VALUE = 29  # some double value

    T_NEG_OP = 32  # !
    T_ADD_OP = 30  # +
    T_SUB_OP = 31  # -

    T_MUL_OP = 33  # *
    T_DIV_OP = 34  # /
    T_MOD_OP = 35  # %
    T_EXP_OP = 36  # **

    T_EQ_REL = 37  # ==
    T_NEQ_REL = 38  # !=

    T_LESS_REL = 39  # <
    T_LEQ_REL = 40  # <=
    T_GREAT_REL = 41  # >
    T_GREQ_REL = 42  # >=

    T_AND_OP = 43  # &&
    T_OR_OP = 44  # ||
    T_XOR_OP = 45  # ^

    T_ASSIGN = 46  # =
    T_ADD_AS = 47  # +=
    T_SUB_AS = 48  # -=
    T_MUL_AS = 49  # *=
    T_DIV_AS = 50  # /=
    T_MOD_AS = 51  # %=
    T_EXP_AS = 52  # **=

    T_AND_AS = 53  # &&=
    T_OR_AS = 54  # ||=
    T_XOR_AS = 55  # ^=

    T_DOT = 56  # .
    T_COMMA = 57  # ,
    T_COLON = 58  # :

    T_CARRIAGE = 59  # \r
    T_NEWLINE = 60  # \n

    T_RIDER = 62  # rider
    T_MOTORCYCLE = 63  # motorcycle

    T_INVALID = 100  # invalid token




class Region(Enum):
    R_IF = 0
    R_ELIF = 1
    R_ELSE = 2
    R_WHILE = 3
    R_METHOD = 4
    R_TYPE = 5

class EstadoDAST(Enum):
    EnProgram=0
    EnAsignacion=1
    EnWhile=2
    EnCondicionIf=3
    EnFuncion=4
    EnArgsdFuncion=8
    EnExpresion=5
    EnTipoEspecial=6
    EnExpresionAssign=7
    EnRedefinition=9
    Condicion=10
    LlamadoAfuncion=11
    CreandoArray=12



class Token:
    def __init__(self, token_type: TokenType, line: int, column: int, value=None):
        self.token_type = token_type
        self.line = line
        self.column = column
        self.value = value

    def __repr__(self):
        return self.string() + ", line {}, column {}".format(self.line, self.column)

    def string(self):
        string = "{}".format(self.token_type.name)
        if self.value is not None:
            string += ": {}".format(self.value)
        return string

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
                                   ["F", TokenType.T_ID, TokenType.T_OPEN_BRACE],[TokenType.T_ID, "I","E",TokenType.T_SEMICOLON]],
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
                                    "E", "U", TokenType.T_CLOSE_BRACKET]]} 
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
                              "A", "Z", "Q", "C", "B", "G", "X", "~", "^"]
        self.first = dict()  # Guardamos los terminales que pertenecen al First de cada produccion posible de nuestra gramatica
        self.follow = {"L": [], "D": [], "I": [], "E": [], "M": [], "Y": [], "J": [], "U": [], "N": [], "@": [],
                       "R": [], "K": [], "T": [], "P": [], "W": [], "S": [], "F": [], "A": [], "Z": [],
                        "Q": [], "C": [], "B": [], "G": [], "X": [], "~": [],
                       "^": []}
                                
        self.completafollow = {"L": [], "D": [], "I": [], "E": [], "M": [], "Y": [], "J": [], "U": [], "N": [], "@": [],
                       "R": [], "K": [], "T": [], "P": [], "W": [], "S": [], "F": [], "A": [], "Z": [],
                        "Q": [], "C": [], "B": [], "G": [], "X": [], "~": [],
                       "^": []} 
                                    # Aqui guardamos los terminales que pertenecen al Follow de cada no terminal
        self.pendiente_follow = []  # Los elementos de esta lista tendran una forma "A,B" lo que significa que todo lo que pertenece al Follow de A tambien pertenece al Folow de B
        self.matriz = [[None for _ in range(len(self.terminales))] for _ in range(len(self.no_terminales))]
        self.lista_producciones = [["L", "D", TokenType.T_SEMICOLON], ["L", "@"], ["L", TokenType.T_CLOSE_BRACE, "N"],
                                   ["L", "W", TokenType.T_SEMICOLON], ["L", TokenType.T_METHOD, "R"],
                                   ["L", "F", TokenType.T_ID, TokenType.T_OPEN_BRACE],["L", TokenType.T_ID, "I","E",TokenType.T_SEMICOLON],
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
                                    TokenType.T_OPEN_BRACKET, "E", "U", TokenType.T_CLOSE_BRACKET]]
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
                        if self.estados[- 1] == (Region.R_IF or Region.R_ELIF):
                            self.estados.pop()
                            self.estados.append(Region.R_ELSE)
                        else:
                            self.error = Error("", "", "", 0, 0)#
                            break
                    elif line[self.i].token_type == TokenType.T_CLOSE_BRACE:
                        if self.i + 1 == len(line) or self.estados[- 1] != (Region.R_IF and Region.R_ELIF):
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
                    if self.estadoDAST==EstadoDAST.EnExpresionAssign and termino!="A" and termino!="U" and termino!="Z":
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
    
    def CreaNododProgram(self,lenline,termino,token):
        if termino=="D":
            nuevonodo = D_Assign()
            self.nodoactual.statements.append(nuevonodo)
            nuevonodo.padre=self.nodoactual
            self.nodoactual=nuevonodo
            self.estadoDAST=EstadoDAST.EnAsignacion
        elif termino==TokenType.T_METHOD:
            nuevonodo= Def_Fun()
            self.nodoactual.statements.append(nuevonodo)
            nuevonodo.padre=self.nodoactual
            self.nodoactual=nuevonodo
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
            self.nodoactual.statements.append(nuevonodo)
            nuevonodo.padre=self.nodoactual
            self.nodoactual=nuevonodo
            self.estadoDAST=EstadoDAST.EnCondicionIf
        elif termino == TokenType.T_WHILE :
            nuevonodo = WhileCond()
            self.nodoactual.statments.append(nuevonodo)
            self.nodoactual=nodonuevo
            self.estadoDAST=EstadoDAST.EnWhile
        elif termino == TokenType.T_RETURN or termino == TokenType.T_BREAK or termino == TokenType.T_CONTINUE :
            nuevonodo = ReturnNode()
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
            nuevonodo = Redefinition()
            self.nodoactual.statements.append(nuevonodo)
            nuevonodo.padre=self.nodoactual
            self.nodoactual=nuevonodo
            self.nodoactual.id=token.value
            self.estadoDAST=EstadoDAST.EnRedefinition
        elif termino == TokenType.T_CLOSE_BRACE :
            self.nodoactual= self.nodoactual.padre
            if isinstance(self.nodoactual,IfCond):
              if self.i+1 == lenline:
                   self.nodoactual=self.nodoactual.padre
                   self.estadoDAST=EstadoDAST.EnProgram
              else:
               self.estadoDAST=EstadoDAST.EnCondicionIf
            if isinstance(self.nodoactual,Def_Fun) or isinstance(self.nodoactual,WhileCond):
              self.nodoactual=self.nodoactual.padre
              self.estadoDAST=EstadoDAST.EnProgram
        

    def EligeTipoDdeclaracion(self,termino,token:Token,line):
        if self.estadoDAST==EstadoDAST.EnAsignacion:
            self.CreaNododAsignacion(termino,token)
        elif self.estadoDAST==EstadoDAST.EnExpresionAssign:
            self.CreaNododExpresion(termino,token,line)
        elif self.estadoDAST==EstadoDAST.EnProgram:
            self.CreaNododProgram(len(line),termino,token)
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
            nuevonodo= NodeE()
            nuevonodo.padre=self.nodoactual.nododreconocimiento
            self.nodoactual.nododreconocimiento.args.append(nuevonodo)
            self.nodoactual.nododreconocimiento=nuevonodo
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
        elif termino==TokenType.T_ADD_AS :
            nuevonodo=AddAs(self.nodoactual.id)
        elif termino==TokenType.T_SUB_AS :
            nuevonodo=SubAs(self.nodoactual.id)
        elif termino==TokenType.T_MUL_AS :
            nuevonodo=MulAs(self.nodoactual.id)
        elif termino==TokenType.T_DIV_AS :
            nuevonodo=DivAs(self.nodoactual.id)
        elif termino==TokenType.T_MOD_AS :
            nuevonodo=ModAs(self.nodoactual.id)
        elif termino==TokenType.T_EXP_AS :
            nuevonodo=ExpAs(self.nodoactual.id)
        elif termino==TokenType.T_AND_AS :
            nuevonodo=AndAs(self.nodoactual.id)
        elif termino==TokenType.T_OR_AS :
            nuevonodo=OrAs(self.nodoactual.id)
        elif termino==TokenType.T_XOR_AS :
            nuevonodo=XorAs(self.nodoactual.id)
        elif termino==TokenType.T_SEMICOLON :
            self.estadoDAST=EstadoDAST.EnProgram
            self.nodoactual= self.nodoactual.padre
            return
        if termino!="I":
         self.nodoactual.op=nuevonodo
         self.estadoDAST=EstadoDAST.EnExpresionAssign
         nodoexpression=Expression()
         self.nodoactual.expr=nodoexpression
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
            nodonuevo.padre=self.nodoactual
            self.nodoactual.body=nodonuevo
            self.nodoactual=nodonuevo
            self.nodoactual.isfuncion=True
            self.estadoDAST=EstadoDAST.EnProgram
            
    def CreaNododIf(self,termino,token:Token):
           if termino == TokenType.T_OPEN_BRACE:
               nuevonodo=Program()
               nuevonodo.padre=self.nodoactual
               self.nodoactual.body=nuevonodo
               self.nodoactual=nuevonodo
               self.estadoDAST=EstadoDAST.EnProgram
           elif termino==TokenType.T_OPEN_PAREN:
               self.estadoDAST=EstadoDAST.Condicion
               nuevonodo= Condition()
               nuevonodo.padre=self.nodoactual
               self.nodoactual=nuevonodo
           elif termino==TokenType.T_ELIF: 
               nuevonodo = IfCond() 
               nuevonodo.padre=self.nodoactual
               self.nodoactual.nodoelse=nuevonodo
               self.nodoactual=nuevonodo  
           elif termino==TokenType.T_ELSE:
               nuevonodo = Program() 
               nuevonodo.padre=self.nodoactual
               self.nodoactual.nodoelse=nuevonodo
               self.nodoactual=nuevonodo
               self.estadoDAST=EstadoDAST.EnProgram

    def CreaNodoCondicion(self,termino,token:Token):
         if termino==TokenType.T_EQ_REL:
             self.nodoactual.comparador=EqRel(self.nodoactual.expression1,self.nodoactual.expression2)
             nuevonodo=Expression()
             self.nodoactual.expression2 = nuevonodo
             nuevonodo.padre=self.nodoactual
             self.nodoactual=nuevonodo
             self.nodoactual.noderaiz=self.nodoactual.nododreconocimiento
             self.estadoDAST=EstadoDAST.EnExpresionAssign
         elif termino==TokenType.T_NEQ_REL:
             self.nodoactual.comparador=NeqRel(self.nodoactual.expression1,self.nodoactual.expression2)
             nuevonodo=Expression()
             self.nodoactual.expression2= nuevonodo
             nuevonodo.padre=self.nodoactual
             self.nodoactual=nuevonodo
             self.nodoactual.noderaiz=self.nodoactual.nododreconocimiento
             self.estadoDAST=EstadoDAST.EnExpresionAssign
         elif termino==TokenType.T_LESS_REL:
             self.nodoactual.comparador=LessRel(self.nodoactual.expression1,self.nodoactual.expression2)
             nuevonodo=Expression()
             self.nodoactual.expression2= nuevonodo
             nuevonodo.padre=self.nodoactual
             self.nodoactual=nuevonodo
             self.nodoactual.noderaiz=self.nodoactual.nododreconocimiento
             self.estadoDAST=EstadoDAST.EnExpresionAssign
         elif termino==TokenType.T_LEQ_REL:
             self.nodoactual.comparador=LeqRel(self.nodoactual.expression1,self.nodoactual.expression2)
             nuevonodo=Expression()
             self.nodoactual.expression2= nuevonodo
             nuevonodo.padre=self.nodoactual
             self.nodoactual=nuevonodo
             self.nodoactual.noderaiz=self.nodoactual.nododreconocimiento
             self.estadoDAST=EstadoDAST.EnExpresionAssign
         elif termino==TokenType.T_GREAT_REL:
             self.nodoactual.comparador=GreatRel(self.nodoactual.expression1,self.nodoactual.expression2)
             nuevonodo=Expression()
             self.nodoactual.expression2= nuevonodo
             nuevonodo.padre=self.nodoactual
             self.nodoactual=nuevonodo
             self.nodoactual.noderaiz=self.nodoactual.nododreconocimiento
             self.estadoDAST=EstadoDAST.EnExpresionAssign
         elif termino==TokenType.T_GREQ_REL:
             self.nodoactual.comparador=GreqRel(self.nodoactual.expression1,self.nodoactual.expression2)
             nuevonodo=Expression()
             self.nodoactual.expression2= nuevonodo
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
            nuevonodo=NodeAdd()
        elif termino==TokenType.T_SUB_OP:
            nuevonodo=NodeSub()
        elif termino==TokenType.T_MUL_OP:
            nuevonodo=NodeMult()
        elif termino==TokenType.T_DIV_OP:
            nuevonodo=NodeDiv()
        elif termino==TokenType.T_MOD_OP:
            nuevonodo=NodeMod()
        elif termino==TokenType.T_EXP_OP:
            nuevonodo=NodeExp()
        elif termino==TokenType.T_COMMA:
             if isinstance (self.nodoactual.padre,Def_Fun):
              self.estadoDAST=EstadoDAST.LlamadoAfuncion
             
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
            if termino==TokenType.T_CLOSE_PAREN and isinstance(self.nodoactual.nododreconocimiento,FunCall):
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
                 nuevonodo.id= token.value
                 self.estadoDAST=EstadoDAST.LlamadoAfuncion
            else:  
                 nuevonodo=Variable(token)
        if termino!=TokenType.T_OPEN_BRACKET:
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


def normaliza(typevar):
        if typevar==VariableType.INT:
          return "int"
        if typevar==VariableType.BOOL:
          return "bool"
        if typevar==VariableType.DOUBLE:
          return "double"
        if typevar==VariableType.STRING:
          return "str"



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

class BodyDFun(Program):

     @staticmethod
     def type() -> str:
        return "CuerpoDFun"

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


def is_number(type) -> bool:
    if type=="int" or type==float:
        return True
    else :
        return False
        

class Op(Node):
    def __init__(self, right_node: Node):
        self.right_node = right_node

    def eval(self, variables: dict):
        return None

    def __repr__(self) -> str:
        return "{}({})".format(self.type(), self.right_node)

    @staticmethod
    def type() -> str:
        return "OP"

class BinOp(Op):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(right_node)
        self.left_node = left_node

    def validate(self,context:Context):
        return self.left_node.validate(context) and self.right_node.validate(context)

    def checktype(self,context:Context):
        typeLeft= self.left_node.checktype(context)
        typeRight=self.right_node.checktype(context)
        if is_number(typeLeft) and is_number(typeRight):
           if typeLeft==typeRight :
             if typeLeft=="int":
                return "int"
             else :
                 return "double"
           else :
               return "double"

    def eval(self, variables: dict):
        left = self.left_node.eval(variables)
        right = self.right_node.eval(variables)
        if is_error(left):
            return left
        if is_error(right):
            return right
        return self.operation(left, right)

    def operation(self, left, right):
        return None

    def __repr__(self) -> str:
        return "{}({}, {})".format(self.type(), self.left_node, self.right_node)

    @staticmethod
    def type() -> str:
        return "BIN_OP"


class AddOp(BinOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def operation(self, left, right):
        if not same_type(left, right):
            return Error("Error", "", "", 0, 0)#
        return left + right

    @staticmethod
    def type() -> str:
        return "ADD"


class ArOp(BinOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def operation(self, left, right):
        if not is_number(left):
            return Error("Error", "", "", 0, 0)#
        if not is_number(right):
            return Error("Error", "", "", 0, 0)#
        self.op(left, right)

    @staticmethod
    def op(left, right):
        return None

    @staticmethod
    def type() -> str:
        return "AR_OP"


class SubOp(ArOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left, right):
        return left - right

    @staticmethod
    def type() -> str:
        return "SUB"

class MulOp(BinOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def operation(self, left, right):
        return left * right

    @staticmethod
    def type() -> str:
        return "MUL"

class DivOp(ArOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left, right):
        if right == 0:
            return Error("Error", "", "", 0, 0)#
        return left / right

    @staticmethod
    def type() -> str:
        return "DIV"


class ModOp(DivOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)
            

    @staticmethod
    def op(left, right):
        if right == 0:
            return Error("Error", "", "", 0, 0)#
        return left % right

    @staticmethod
    def type() -> str:
        return "MOD"

class ExpOp(ArOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left, right):
        return left ** right

    @staticmethod
    def type() -> str:
        return "EXP"

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

class NodeValue(Node):
    padre = None
    def __init__(self,token:Token):
       self.ast= token.value

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



class NodeB(Node):
   def __init__(self):
    self.padre = None
    self.hijos= list()  
    self.ast = None 
   
   def refreshAST(self):
    if len(self.hijos)==2:
        self.ast=self.hijos[1].ast
    

class NodeX:
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




class Assign(Node):
    def __init__(self, id_node: Node):
        self.id_node = id_node
        self.expression:Expression = None

    def eval(self, variables: dict):
        var_id = self.id_node.id()
        if not variables.keys().__contains__(var_id):
            return Error("Error", "", "", 0, 0)#
        value = self.expression.eval(variables)
        if is_error(value):
            return value
        return self.review(variables, var_id, value)

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

    def checktype(self,context:Context):
        
        if self.expression.checktype(context)==normaliza(context.gettypevar(self.idnode)):
            return True
        else :
            return False

    def __repr__(self):
        return "{}_AS({}, {})".format(self.type(), self.id_node, self.expression)

    @staticmethod
    def type() -> str:
        return "OP"

class AddAs(OpAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    @staticmethod
    def review(variables: dict, var_id: str, value):
        if not same_type(variables[var_id], value):
            raise Exception#
        variables[var_id] += value
        return variables[var_id]

    @staticmethod
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

    @staticmethod
    def operation(variables: dict, var_id: str, value):
        variables[var_id] -= value
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "SUB"


class MulAs(OpAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    @staticmethod
    def review(variables: dict, var_id: str, value):
        variables[var_id] *= value
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "MUL"


class DivAs(ArAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    @staticmethod
    def operation(variables: dict, var_id: str, value):
        if value == 0:
            return Error("Error", "", "", 0, 0)#
        variables[var_id] /= value
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "DIV"


class ModAs(DivAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    @staticmethod
    def operation(variables: dict, var_id: str, value):
        if value == 0:
            return Error("Error", "", "", 0, 0)#
        variables[var_id] %= value
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "MOD"


class ExpAs(ArAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    @staticmethod
    def operation(variables: dict, var_id: str, value):
        variables[var_id] **= value
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "EXP"


class BoolAs(OpAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    def operation(self, variables: dict, var_id: str, value):
        if not is_bool(variables[var_id]):
            return Error("Error", "", "", 0, 0)#
        if not is_bool(value):
            return Error("Error", "", "", 0, 0)#
        return self.op(variables, var_id, value)

    @staticmethod
    def op(variables: dict, var_id: str, value):
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "BOOL"


class AndAs(BoolAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    @staticmethod
    def op(variables: dict, var_id: str, value):
        variables[var_id] &= value
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "AND"


class OrAs(BoolAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    @staticmethod
    def op(variables: dict, var_id: str, value):
        variables[var_id] |= value
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "OR"


class XorAs(BoolAs):
    def __init__(self, id_node: Node):
        self.idnode=id_node
        self.expression:Expression = None

    @staticmethod
    def op(variables: dict, var_id: str, value):
        variables[var_id] ^= value
        return variables[var_id]

    @staticmethod
    def type() -> str:
        return "XOR"

class Rel(BinOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def operation(self, left, right) -> bool:
        return same_type(left, right) and self.op(left, right)

    def checktype(self, context):
        if self.right_node==None and self.left_node.checktype(context)=="bool" :
              return True     
        if self.left_node.checktype(context) == self.right_node.checktype(context):
           return True
        return False

    @staticmethod
    def op(left, right) -> bool:
        return False

    @staticmethod
    def type() -> str:
        return "EQ"


class EqRel(Rel):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left, right) -> bool:
        return left == right

    @staticmethod
    def type() -> str:
        return "EQ"


class NeqRel(Rel):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left, right) -> bool:
        return left != right

    @staticmethod
    def type() -> str:
        return "NEQ"


class LessRel(Rel):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left, right) -> bool:
        return left < right

    @staticmethod
    def type() -> str:
        return "LESS"


class LeqRel(Rel):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left, right) -> bool:
        return left <= right

    @staticmethod
    def type() -> str:
        return "LEQ"


class GreatRel(Rel):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left, right) -> bool:
        return left > right

    @staticmethod
    def type() -> str:
        return "GREAT"


class GreqRel(Rel):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left, right) -> bool:
        return left >= right

    @staticmethod
    def type() -> str:
        return "GREQ"

class BoolOp(BinOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    def operation(self, left, right):
        if not is_bool(left):
            return Error("Error", "", "", 0, 0)#
        if not is_bool(right):
            return Error("Error", "", "", 0, 0)#
        self.op(left, right)

    @staticmethod
    def op(left: bool, right: bool) -> bool:
        return False

    @staticmethod
    def type() -> str:
        return "BOOL_OP"


class AndOp(BoolOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left: bool, right: bool) -> bool:
        return left and right

    @staticmethod
    def type() -> str:
        return "AND"


class OrOp(BoolOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left: bool, right: bool) -> bool:
        return left or right

    @staticmethod
    def type() -> str:
        return "OR"


class XorOp(BoolOp):
    def __init__(self, left_node: Node, right_node: Node):
        super().__init__(left_node, right_node)

    @staticmethod
    def op(left: bool, right: bool) -> bool:
        return left ^ right

    @staticmethod
    def type() -> str:
        return "XOR"
