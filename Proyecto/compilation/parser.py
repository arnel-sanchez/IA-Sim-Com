def CreateLines(tokens:[Token]):       
        lines=0
        cursorDtokens=0
        saveLines=None
        line=None
        
        while cursorDtokens<len(tokens) :
             
            if tokens[cursorDtokens].TokenType == TokenType.T_WHILE or TokenType.T_IF or TokenType.T_METHOD or TokenType.T_ELIF or TokenType.T_ELSE :
                  while tokens[cursorDtokens].TokenType != TokenType.T_OPEN_BRACE :
                  
                   line.append(tokens[cursorDtokens])
                   cursorDtokens+=1
                  line.append(tokens[cursorDtokens])
                  cursorDtokens+=1

            elif tokens[cursorDtokens].TokenType == TokenType.T_CLOSE_BRACE :
                  line.append(tokens[cursorDtokens])
                  cursorDtokens+=1
                  if (cursorDtokens<len(tokens)) and (tokens[cursorDtokens].TokenType==TokenType.T_ELSE or TokenType.T_ELIF):
                      while tokens[cursorDtokens].TokenType!=Tokentype.T_OPEN_BRACE :
                              line.append(tokens[cursorDtokens])
                              cursorDtokens+=1
            else :                
                while tokens[cursorDtokens].token_type!=TokenType.T_SEMICOLON :
                
                 line.append(tokens[cursorDtokens])
                 cursorDtokens+=1
                 
                line.append(tokens[cursorDtokens])
                cursorDtokens+=1
            saveLines.append(line)
            line=None
            lines+=1
                
    
        return saveLines,lines    

class Parser :

       def __init__(self) :

            self.Variables = dict([])  #Scope de variables  
            self.Producciones = {"L": [["D",TokenType.T_SEMICOLON],["@"],[TokenType.T_CLOSE_BRACE,"N"],["W",TokenType.T_SEMICOLON],[TokenType.T_METHOD,"R"],["F",TokenType.T_ID,TokenType.T_OPEN_BRACE]], "D": [["T",TokenType.T_ID,TokenType.T_ASSIGN,"E"],[TokenType.T_ARRAY,"T",TokenType.T_ID,TokenType.T_ASSIGN,TokenType.T_OPEN_BRACKET,"A",TokenType.T_CLOSE_BRACKET],[TokenType.T_ID,"O","E"]],"T":[[TokenType.T_STRING],[TokenType.T_INT],[TokenType.T_DOUBLE],[TokenType.T_BOOL]],"R":[["K",TokenType.T_M_ID,TokenType.T_OPEN_PAREN,
             "P",TokenType.T_CLOSE_PAREN,TokenType.T_OPEN_BRACE]],"K":[["T"],[TokenType.T_VOID]],"P":[["E","X"],["e"]],"X":[[TokenType.TokenType.T_COMMA,"E","X"],["e"]],"@":[[TokenType.T_IF, TokenType.T_OPEN_PAREN,"Q", TokenType.T_CLOSE_PAREN, TokenType.T_OPEN_BRACE],[ TokenType.T_WHILE, TokenType.T_OPEN_PAREN,"Q", TokenType.T_CLOSE_PAREN, TokenType.T_OPEN_BRACE]],"N":[[TokenType.T_ELSE,TokenType.T_OPEN_BRACE],[TokenType.T_ELIF,TokenType.T_OPEN_PAREN,"Q", TokenType.T_CLOSE_PAREN, TokenType.T_OPEN_BRACE],["e"]],"W":[[TokenType.T_CONTINUE],[TokenType.T_BREAK],[TokenType.T_RETURN]],"F":[[TokenType.T_RIDER],[TokenType.T_MOTORCICLE]],"A":[[TokenType.T_ID,"B"],[]]}
            self.Terminales = ["bool","break","continue","double","elif","else",
                              "false","if","include","int","method","null","return","string","true","void","while","<",">","<=",">=",":",";",",","(",")","{","}","&&","||","==","!","=","/=","-","+","+=","-=","*","/","!=","**","%","*=","/=","%=","**=","&&=","||=","motorcycle","rider","track","weather","angle","brakes", "lap","length","speed","temperature","skill","tyres"] 
            
            self.NoTerminales= ["E","M","C","D"]
            self.First=dict([])   #Guardamos los terminales que pertenecen al First de cada produccion posible de nuestra gramatica
            self.Follow={"A":["a","b","c"],"B":["n","m","l"],"C":["i","o","t"]}     #Aqui guardamos los terminales que pertenecen al Follow de cada no terminal 
            self.PendienteDfollow= []   #Los elementos de esta lista tendran una forma "A,B" lo que significa que todo lo que pertenece al Follow de A tambien pertenece al Folow de B
            self.Estados=[] #Aqui guardamos los estados en forma de string , de forma que si el ultimo estado de la lista es el estado en el que estoy y si no hay estados en la lista ent estamos fuera de cualquier ambito del programa 

            self.ListaDProducciones=[]
            self.HazFirst("L")  
            self.HazFollow()          
            ConstruyeTablaLL()

           #los terminales de la gramatica son estos que guardamos en el diccionario Terminales junto a las variables
           # y funciones que se guardan a medida que se crean en el diccionario Variables ,con su tipo , si se guarda una funcion
           #se guardaria primero los tipos de los parametros de dicha funcion y luego el tipo de retorno. 

      # def Parsing(tokens:[Token]))
       
       def HazFirst(self,Cadena) :
             self.First.setdefault(Cadena,[])          
             i=0
             for pr in self.Producciones[Cadena]:
                self.First.setdefault(Cadena,[]) 
                if self.NoTerminales.count(pr[i])==1:                                      
                    
                    self.HazFirst(pr[i])
                    self.First[Cadena].extend(self.First[pr[i]])
                    self.First[pr].extend(self.First[pr[i]])
                    while SeVaEnEpsilon(pr[i])&i<len(pr) :
                      i+=1
                      self.HazFirst(pr[i])
                      self.First[Cadena].extend(self.First[pr[i]]) 
                      self.First[pr].extend(self.First[pr[i]])
                    i=0
                else:
                   self.First[Cadena].append(pr[i])
                   self.First[pr].append(pr[i])
                   break

       def SeVaEnEpsilon(self,NoTerminal) :
           
           if self.NoTerminales.count(NoTerminal)==1:  
                 for pr in self.Producciones[NoTerminal]:
                   j=0
                   lenDproduccion=len(pr)
                   while j<lenDproduccion :
                            if SeVaEnEpsilon(pr[j]) :  
                                   j+=1
                            else: break
                   if j==(len(pr)-1): return True
                 
                 return False
                                   
           else : 
               if NoTerminal=="e": return True
               return False

       def HazFollow(self) :
           TerminalesParaElFollow=list()             # Aqui voy teniendo los posibles terminales que pueden pertenecer al follow de los no terminales que voy revisando
           for pr in self.ListaDProducciones:
            ExisteUltimoTerminal=True                 #Esta variable es para identificar los casos en que lo ultimo que me queda en mi produccion pueda ser un No terminal y por lo tanto el Follow de la cabeza de la produccion sera subconjunyto del Follow del no terminal 
            i=(len(pr)-1)
            while i>=1 :              
                  if self.NoTerminales.count(pr[i])==1:
                    if(len(TerminalesParaElFollow)>0) :
                         self.Follow[pr[i]].extend(TerminalesParaElFollow)
                    if ExisteUltimoTerminal==True :
                        self.PendienteDfollow.append("{},{}".format(pr[0],pr[i]))                      
                    if SeVaEnEpsilon(pr[i]) :
                      TerminalesParaElFollow.extend(self.First(pr[i]))
                    else:
                      TerminalesParaElFollow.clear()
                      TerminalesParaElFollow.extend(self.First(pr[i]))
                      ExisteUltimoTerminal=False
                  else : 
                      ExisteUltimoTerminal=False
                      TerminalesParaElFollow.clear()
                      TerminalesParaElFollow.append(pr[i]) 
              
                  i-=1
              
       def CompletaFollows(self): 
         for follow in self.PendienteDfollow:
            self.Follow[follow[2]].extend(self.Follow[follow[0]])

       def ConstruyeTablaLL(self):
            self.matriz=[[None for i in range(len(self.Terminales))]for i in range(len(self.NoTerminales))]
            fila=0
            columna=0
            for x in self.NoTerminales:
                for y in self.Terminales:
                  i=0 
                  if y!="e":
                   while i<len(self.Producciones[x]):
                    if self.First[self.Producciones[x][i]].count(y)>0: 
                        self.matriz[fila][columna]=self.Producciones[x][i] 
                    i+=1
                  columna+=1
                fila+=1


       def Parsea(self,Line,i,Cadena) :
           
           for Termino in Cadena: 
              if(i<len(Line)): 
               if i==0 :
                if len(self.Estados)!=0:
                    Estado=self.Estados[len(self.Estados)-1]
                    if Estado=="EnTipo":
                        if Line[i].TokenType==TokenType.T_WHILE or TokenType.T_IF or TokenType.T_ELIF or TokenType.T_ELSE :
                            self.errores.append("Error")
                            break
                         
                    elif Estado=="EnRegion":
                        if Line[i].TokenType==TokenType.T_METHOD :
                           self.errores.append("Error")
                           break
               
               
               if Termino==Line[i].TokenType:                 
                   if Line[i].TokenType==TokenType.T_WHILE or TokenType.T_IF or TokenType.T_ELIF or TokenType.T_ELSE :
                       self.Estados.append("EnRegionWhile")
                   elif Line[i].TokenType==TokenType.T_IF:
                       self.Estados.append("EnRegionIF")
                   elif Line[i].TokenType==TokenType.T_ELIF:
                       self.Estados.pop()
                       self.Estados.append("EnRegionElif")
                   elif Line[i].TokenType==TokenType.T_ELSE :
                       self.Estados.pop()
                       self.Estados.append("EnRegionElse")
                   elif Line[i].TokenType==TokenType.Tipo :
                       self.Estados.append("EnRegionTipo")#Aqui falta agregar-----------------cuando es dentro de un tipo
                   elif Line[i].TokenType== TokenType.T_ClOSE_BRACE :
                       if self.Estados[len(self.Estados)-1]!="EnRegionIF"and"EnRegionElif" :
                           self.Estados.pop()
                   i+=1
                   continue              
               IndiceNT=self.NoTerminales.index(Termino)
               IndiceT= self.Terminales.index(Line[i])
               
               if matriz[IndiceNT][IndiceT]!=None and "e" :
                   Parsea(Line,i,matriz[IndiceNT][IndiceT])
               elif matriz[IndiceNT][IndiceT]!="e" :
                   self.errores.append("Error") #Aqui debemos agregar el error , con ello la linea y la columna que fue para posteriormente comunicarselo al usuario

              else : 
                     break

 #Debemos crear el Parser en nuestro main.py y llamar al metodo Parsea Que se encarga de Parsear las Lineas que tenemos 