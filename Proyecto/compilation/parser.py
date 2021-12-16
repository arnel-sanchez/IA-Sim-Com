from compilation.tokens import Token, TokenType


def split_lines(tokens: [Token]) -> [[TokenType]]:
    t_pointer = 0
    current_line = []
    lines = []
    while t_pointer < len(tokens):
        if tokens[t_pointer].token_type == (TokenType.T_IF or TokenType.T_ELIF or TokenType.T_ELSE or
                                            TokenType.T_WHILE or TokenType.T_METHOD):
            t_pointer = loop(tokens, t_pointer, current_line, TokenType.T_OPEN_BRACE)
        elif tokens[t_pointer].token_type == TokenType.T_CLOSE_BRACE:
            lines.append(current_line)
            current_line = [tokens[t_pointer]]
            t_pointer += 1
            if t_pointer < len(tokens) and tokens[t_pointer].token_type == (TokenType.T_ELIF or TokenType.T_ELSE):
                t_pointer = loop(tokens, t_pointer, current_line, TokenType.T_OPEN_BRACE)
        else:
            t_pointer = loop(tokens, t_pointer, current_line, TokenType.T_SEMICOLON)
        lines.append(current_line)
        current_line = []
    return lines


def loop(tokens: [Token], t_pointer: int, current_line: [Token], comparator: TokenType):
    while t_pointer < len(tokens):
        current_line.append(tokens[t_pointer])
        if tokens[t_pointer].token_type == comparator:
            return t_pointer + 1
        t_pointer += 1
    return t_pointer


class Parser:
    def __init__(self):
        self.errores = []
        self.variables = dict()  # Scope de variables
        self.producciones = {"L": [["D", TokenType.T_SEMICOLON], ["@"], [TokenType.T_CLOSE_BRACE, "N"],
                                   ["W", TokenType.T_SEMICOLON], [TokenType.T_METHOD, "R"],
                                   ["F", TokenType.T_ID, TokenType.T_OPEN_BRACE]],
                             "D": [[TokenType.T_BOOL, TokenType.T_ID, TokenType.T_ASSIGN, "G"],
                                   [TokenType.T_INT, TokenType.T_ID, TokenType.T_ASSIGN, "B"],
                                   [TokenType.T_STRING, TokenType.T_ID, TokenType.T_ASSIGN, "X"],
                                   [TokenType.T_DOUBLE, TokenType.T_ID, TokenType.T_ASSIGN, "E"],
                                   [TokenType.T_ARRAY, TokenType.T_BOOL, TokenType.T_ID, TokenType.T_ASSIGN,
                                    TokenType.T_OPEN_BRACKET, "G", "M", TokenType.T_CLOSE_BRACKET],
                                   [TokenType.T_ARRAY, TokenType.T_INT, TokenType.T_ID, TokenType.T_ASSIGN,
                                    TokenType.T_OPEN_BRACKET, "B", "Y", TokenType.T_CLOSE_BRACKET],
                                   [TokenType.T_ARRAY, TokenType.T_STRING, TokenType.T_ID, TokenType.T_ASSIGN,
                                    TokenType.T_OPEN_BRACKET, "X", "J", TokenType.T_CLOSE_BRACKET],
                                   [TokenType.T_ARRAY, TokenType.T_DOUBLE, TokenType.T_ID, TokenType.T_ASSIGN,
                                    TokenType.T_OPEN_BRACKET, "E", "U", TokenType.T_CLOSE_BRACKET],
                                   [TokenType.T_ID, "Ñ"]],
                             "T": [[TokenType.T_STRING], [TokenType.T_INT], [TokenType.T_DOUBLE], [TokenType.T_BOOL]],
                             "R": [["K", TokenType.T_ID, TokenType.T_OPEN_PAREN, "P", TokenType.T_CLOSE_PAREN,
                                    TokenType.T_OPEN_BRACE]],
                             "K": [["T"], [TokenType.T_VOID]],
                             "P": [["T", TokenType.T_ID, "N"], ["e"]],
                             "~": [[TokenType.T_COMMA, "T", TokenType.T_ID, "N"], ["e"]],
                             "@": [[TokenType.T_IF, TokenType.T_OPEN_PAREN, "G", TokenType.T_CLOSE_PAREN,
                                   TokenType.T_OPEN_BRACE],
                                   [TokenType.T_WHILE, TokenType.T_OPEN_PAREN, "G", TokenType.T_CLOSE_PAREN,
                                    TokenType.T_OPEN_BRACE]],
                             "N": [[TokenType.T_ELSE, TokenType.T_OPEN_BRACE],
                                   [TokenType.T_ELIF, TokenType.T_OPEN_PAREN, "G", TokenType.T_CLOSE_PAREN,
                                    TokenType.T_OPEN_BRACE], ["e"]],
                             "W": [[TokenType.T_CONTINUE], [TokenType.T_BREAK], [TokenType.T_RETURN]],
                             "F": [[TokenType.T_RIDER], [TokenType.T_MOTORCYCLE]],
                             "A": [[TokenType.T_OPEN_PAREN, "Z", TokenType.T_CLOSE_PAREN], ["e"]],
                             "Z": [["#", "$"]],
                             "$": [["e"], [TokenType.T_COMMA, "Z"]],
                             "#": [["E"], ["X"], ["B"], ["G"]],
                             "H": [["e"], ["O", "E"]],
                             "O": [[TokenType.T_ADD_OP], [TokenType.T_SUB_OP], [TokenType.T_MUL_OP],
                                   [TokenType.T_DIV_OP], [TokenType.T_MOD_OP], [TokenType.T_EXP_OP]],
                             "?": [["e"], ["O", "B"]],
                             "I": [[TokenType.T_ADD_AS], [TokenType.T_SUB_AS], [TokenType.T_DIV_AS],
                                   [TokenType.T_MUL_AS], [TokenType.T_MOD_AS], [TokenType.T_EXP_AS]],
                             "V": [["B"], ["E"]],
                             "Ñ": [["I", "V"], [TokenType.T_ASSIGN, "#"]],
                             "Q": [[TokenType.T_EQ_REL], [TokenType.T_NEQ_REL]],
                             "C": [[TokenType.T_GREQ_REL], [TokenType.T_GREAT_REL], [TokenType.T_LESS_REL],
                                   [TokenType.T_LEQ_REL], ["Q"]],
                             "M": [["e"], [TokenType.T_COMMA, "G", "M"]],
                             "Y": [["e"], [TokenType.T_COMMA, "B", "Y"]],
                             "J": [["e"], [TokenType.T_COMMA, "X", "J"]],
                             "U": [["e"], [TokenType.T_COMMA, "E", "U"]],
                             "X": [[TokenType.T_ID, "A"], [TokenType.T_S_VALUE]],
                             "E": [["e"]],
                             "B": [["e"]],
                             "G": [["e"]],
                             "S": [["e"]]}  # Faltan las expresiones double , int y las condicionales
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
        self.no_terminales = ["L", "D", "I", "E", "M", "Y", "J", "U", "N", "@", "R", "K", "T", "P", "W", "S", "F", "V",
                              "A", "Z", "#", "H", "O", "Q", "C", "B", "G", "X", "~", "$", "?", "Ñ"]
        self.first = dict()  # Guardamos los terminales que pertenecen al First de cada produccion posible de nuestra gramatica
        self.follow = {"L": [], "D": [], "I": [], "E": [], "M": [], "Y": [], "J": [], "U": [], "N": [], "@": [],
                       "R": [], "K": [], "T": [], "P": [], "W": [], "S": [], "F": [], "V": [], "A": [], "Z": [],
                       "#": [], "H": [], "O": [], "Q": [], "C": [], "B": [], "G": [], "X": [], "~": [], "$": [],
                       "?": [], "Ñ": []}  # Aqui guardamos los terminales que pertenecen al Follow de cada no terminal
        self.pendiente_follow = []  # Los elementos de esta lista tendran una forma "A,B" lo que significa que todo lo que pertenece al Follow de A tambien pertenece al Folow de B
        self.estados = []  # Aqui guardamos los estados en forma de string , de forma que si el ultimo estado de la lista es el estado en el que estoy y si no hay estados en la lista ent estamos fuera de cualquier ambito del programa
        self.matriz = [[None for _ in range(len(self.terminales))] for _ in range(len(self.no_terminales))]
        self.first_producciones_calculado = False  # Esta variable booleana me sirve calcular los first restantes que luego me hacen falta para los Follows
        self.lista_producciones = [["L", "D", TokenType.T_SEMICOLON], ["L", "@"], ["L", TokenType.T_CLOSE_BRACE, "N"],
                                   ["L", "W", TokenType.T_SEMICOLON], ["L", TokenType.T_METHOD, "R"],
                                   ["L", "F", TokenType.T_ID, TokenType.T_OPEN_BRACE],
                                   ["D", TokenType.T_BOOL, TokenType.T_ID, TokenType.T_ASSIGN, "G"],
                                   ["D", TokenType.T_INT, TokenType.T_ID, TokenType.T_ASSIGN, "B"],
                                   ["D", TokenType.T_STRING, TokenType.T_ID, TokenType.T_ASSIGN, "X"],
                                   ["D", TokenType.T_DOUBLE, TokenType.T_ID, TokenType.T_ASSIGN, "E"],
                                   ["D", TokenType.T_ARRAY, TokenType.T_BOOL, TokenType.T_ID, TokenType.T_ASSIGN,
                                    TokenType.T_OPEN_BRACKET, "G", "M", TokenType.T_CLOSE_BRACKET],
                                   ["D", TokenType.T_ARRAY, TokenType.T_INT, TokenType.T_ID, TokenType.T_ASSIGN,
                                    TokenType.T_OPEN_BRACKET, "B", "Y", TokenType.T_CLOSE_BRACKET],
                                   ["D", TokenType.T_ARRAY, TokenType.T_STRING, TokenType.T_ID, TokenType.T_ASSIGN,
                                    TokenType.T_OPEN_BRACKET, "X", "J", TokenType.T_CLOSE_BRACKET],
                                   ["D", TokenType.T_ARRAY, TokenType.T_DOUBLE, TokenType.T_ID, TokenType.T_ASSIGN,
                                    TokenType.T_OPEN_BRACKET, "E", "U", TokenType.T_CLOSE_BRACKET],
                                   ["D", TokenType.T_ID, "Ñ"], ["T", TokenType.T_STRING], ["T", TokenType.T_INT],
                                   ["T", TokenType.T_DOUBLE], ["T", TokenType.T_BOOL],
                                   ["R", "K", TokenType.T_ID, TokenType.T_OPEN_PAREN,
                                    "P", TokenType.T_CLOSE_PAREN, TokenType.T_OPEN_BRACE], ["K", "T"],
                                   ["K", TokenType.T_VOID], ["P", "T", TokenType.T_ID, "N"], ["P", "e"],
                                   ["~", TokenType.T_COMMA, "T", TokenType.T_ID, "N"], ["~", "e"],
                                   ["@", TokenType.T_IF, TokenType.T_OPEN_PAREN, "G", TokenType.T_CLOSE_PAREN,
                                    TokenType.T_OPEN_BRACE],
                                   ["@", TokenType.T_WHILE, TokenType.T_OPEN_PAREN, "G", TokenType.T_CLOSE_PAREN,
                                    TokenType.T_OPEN_BRACE], ["N", TokenType.T_ELSE, TokenType.T_OPEN_BRACE],
                                   ["N", TokenType.T_ELIF, TokenType.T_OPEN_PAREN, "G", TokenType.T_CLOSE_PAREN,
                                    TokenType.T_OPEN_BRACE], ["N", "e"], ["W", TokenType.T_CONTINUE],
                                   ["W", TokenType.T_BREAK], ["W", TokenType.T_RETURN], ["F", TokenType.T_RIDER],
                                   ["F", TokenType.T_MOTORCYCLE],
                                   ["A", TokenType.T_OPEN_PAREN, "Z", TokenType.T_CLOSE_PAREN], ["A", "e"],
                                   ["Z", "#", "$"], ["$", "e"], ["$", TokenType.T_COMMA, "Z"], ["#", "E"], ["#", "X"],
                                   ["#", "B"], ["#", "G"], ["H", "e"], ["H", "O", "E"], ["O", TokenType.T_ADD_OP],
                                   ["O", TokenType.T_SUB_OP], ["O", TokenType.T_MUL_OP], ["O", TokenType.T_DIV_OP],
                                   ["O", TokenType.T_MOD_OP], ["O", TokenType.T_EXP_OP], ["?", "e"], ["?", "O", "B"],
                                   ["I", TokenType.T_ADD_AS], ["I", TokenType.T_SUB_AS], ["I", TokenType.T_DIV_AS],
                                   ["I", TokenType.T_MUL_AS], ["I", TokenType.T_MOD_AS], ["I", TokenType.T_EXP_AS],
                                   ["V", "B"], ["V", "E"], ["Ñ", "I", "V"], ["Ñ", TokenType.T_ASSIGN, "#"],
                                   ["Q", TokenType.T_EQ_REL], ["Q", TokenType.T_NEQ_REL], ["C", TokenType.T_GREQ_REL],
                                   ["C", TokenType.T_GREAT_REL], ["C", TokenType.T_LESS_REL],
                                   ["C", TokenType.T_LEQ_REL], ["C", "Q"], ["M", "e"],
                                   ["M", TokenType.T_COMMA, "G", "M"], ["Y", "e"], ["Y", TokenType.T_COMMA, "B", "Y"],
                                   ["J", "e"], ["J", TokenType.T_COMMA, "X", "J"], ["U", "e"],
                                   ["U", TokenType.T_COMMA, "E", "U"], ["X", TokenType.T_ID, "A"],
                                   ["X", TokenType.T_S_VALUE]]
        self.hacer_first("L")
        self.first_producciones_calculado = True
        self.calcular_first_restantes()
        self.hacer_follow()
        self.completar_follows()
        self.construir_tabla_LL()
        # los terminales de la gramatica son estos que guardamos en el diccionario Terminales junto a las variables
        # y funciones que se guardan a medida que se crean en el diccionario Variables ,con su tipo , si se guarda una funcion
        # se guardaria primero los tipos de los parametros de dicha funcion y luego el tipo de retorno.

    #def parsing(tokens:[Token]))

    def hacer_first(self, cadena):
        if self.first.keys().isdisjoint(cadena):
            self.first[cadena] = []
        i = 0
        for pr in self.producciones[cadena]:
            if not self.first_producciones_calculado:
                self.first.setdefault(self.key(pr), [])
            if self.no_terminales.count(pr[i]) == 1:
                self.hacer_first(pr[i])
                self.first[cadena].extend(self.first[pr[i]])
                if not self.first_producciones_calculado and len(pr) > 1:
                    self.first[self.key(pr)].extend(self.first[pr[i]])
                while self.se_va_en_epsilon(pr[i]) and i < len(pr):
                    i += 1
                    if i == len(pr):
                        break
                    if self.no_terminales.count(pr[i]) == 1:
                        self.hacer_first(pr[i])
                        self.first[cadena].extend(self.first[pr[i]])
                        if not self.first_producciones_calculado:
                            self.first[self.key(pr)].extend(self.first[pr[i]])
                    else:
                        self.first[cadena].append(pr[i])
                        break
                i = 0
            else:
                if self.first[cadena].count(pr[i]) == 0:
                    self.first[cadena].append(pr[i])
                if not self.first_producciones_calculado:
                    self.first[self.key(pr)].append(pr[i])

    def se_va_en_epsilon(self, no_terminal) -> bool:
        if self.no_terminales.count(no_terminal) == 1:
            for pr in self.producciones[no_terminal]:
                j = 0
                len_produccion = len(pr)
                while j < len_produccion:
                    if self.se_va_en_epsilon(pr[j]):
                        j += 1
                    else:
                        break
                if j == len(pr):
                    return True
            return False
        else:
            return no_terminal == "e"
        #return True

    def calcular_first_restantes(self):
        for x in self.no_terminales:
            if self.first.keys().isdisjoint(x):
                self.hacer_first(x)

    def hacer_follow(self):
        terminales_para_follow = list()  # Aqui voy teniendo los posibles terminales que pueden pertenecer al follow de los no terminales que voy revisando
        for pr in self.lista_producciones:
            existe_ultimo_terminal = True  # Esta variable es para identificar los casos en que lo ultimo que me queda en mi produccion pueda ser un No terminal y por lo tanto el Follow de la cabeza de la produccion sera subconjunyto del Follow del no terminal
            i = (len(pr) - 1)
            while i >= 1:
                if self.no_terminales.count(pr[i]) == 1:
                    if len(terminales_para_follow) > 0:
                        self.follow[pr[i]].extend(terminales_para_follow)
                    if existe_ultimo_terminal:
                        self.pendiente_follow.append("{},{}".format(pr[0], pr[i]))
                    if self.se_va_en_epsilon(pr[i]):
                        terminales_para_follow.extend(self.first[pr[i]])
                    else:
                        terminales_para_follow.clear()
                        terminales_para_follow.extend(self.first[pr[i]])
                        existe_ultimo_terminal = False
                else:
                    existe_ultimo_terminal = False
                    terminales_para_follow.clear()
                    terminales_para_follow.append(pr[i])
                i -= 1

    def completar_follows(self):
        for follow in self.pendiente_follow:
            self.follow[follow[2]].extend(self.follow[follow[0]])

    def construir_tabla_LL(self):
        fila = 0
        for x in self.no_terminales:
            columna = 0
            for y in self.terminales:
                i = 0
                if y != "e":
                    while i < len(self.producciones[x]):
                        esta = self.first.get(self.key(self.producciones[x][i]), "NoEsta")
                        if esta != "NoEsta":
                            if self.first[self.key(self.producciones[x][i])].count(y) > 0:
                                self.matriz[fila][columna] = self.producciones[x][i]
                                break
                        i += 1
                columna += 1
            fila += 1

    def parsear(self, line, i, cadena):
        for termino in cadena:
            if i < len(line):
                if i == 0:
                    if len(self.estados) != 0:
                        estado = self.estados[len(self.estados) - 1]
                        if estado == "EnTipo":
                            if line[i].token_type == (TokenType.T_WHILE or TokenType.T_IF or TokenType.T_ELIF or
                                                      TokenType.T_ELSE):
                                self.errores.append("Error")
                                break
                        elif estado == "EnRegion":
                            if line[i].token_type == TokenType.T_METHOD:
                                self.errores.append("Error")
                                break
                if termino == line[i].token_type:
                    if line[i].token_type == (TokenType.T_WHILE or TokenType.T_IF or TokenType.T_ELIF or
                                              TokenType.T_ELSE):
                        self.estados.append("EnRegionWhile")
                    elif line[i].token_type == TokenType.T_IF:
                        self.estados.append("EnRegionIF")
                    elif line[i].token_type == TokenType.T_ELIF:
                        self.estados.pop()
                        self.estados.append("EnRegionElif")
                    elif line[i].token_type == TokenType.T_ELSE:
                        self.estados.pop()
                        self.estados.append("EnRegionElse")
                    elif line[i].token_type == (TokenType.T_RIDER or TokenType.T_MOTORCYCLE):
                        self.estados.append("EnRegionTipo")  # Aqui falta agregar-----------------cuando es dentro de un tipo
                    elif line[i].token_type == TokenType.T_CLOSE_BRACE:
                        if self.estados[len(self.estados) - 1] != ("EnRegionIF" and "EnRegionElif"):
                            self.estados.pop()
                    i += 1
                    continue
                indice_nt = self.no_terminales.index(termino)
                indice_t = self.terminales.index(line[i].token_type)
                if self.matriz[indice_nt][indice_t] != (None and "e"):
                    self.parsear(line, i, self.matriz[indice_nt][indice_t])
                elif self.matriz[indice_nt][indice_t] != "e":
                    self.errores.append("Error")  # Aqui debemos agregar el error , con ello la linea y la columna que fue para posteriormente comunicarselo al usuario
            else:
                break

# Debemos crear el Parser en nuestro main.py y llamar al metodo Parsea Que se encarga de Parsear las Lineas que tenemos
    def key(self, pr):
        produccion = ""
        i = 0
        while i < len(pr):
            if isinstance(pr[i], TokenType):
                produccion += "'" + pr[i].name + "'"
            else:
                produccion += pr[i]
            i += 1
        return produccion

    def mask(self, lines: [[Token]]):
        for line in lines:
            self.parsear(line, 0, "L")


